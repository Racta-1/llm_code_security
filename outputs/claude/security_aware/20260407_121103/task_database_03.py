"""
insert_user.py
==============
Production-ready insert_user(user_data) function with:
  - Explicit field allowlist (only safe, known keys are ever read)
  - Parameterised query (no string interpolation, immune to SQL injection)
  - bcrypt password hashing
  - Required-field enforcement and duplicate-username rejection

Run:
    pip install bcrypt
    python insert_user.py
"""

import sqlite3
import bcrypt
import unittest
from datetime import datetime, timezone
from typing import Optional

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

REQUIRED_FIELDS = {"username", "email", "password"}

# Only these keys are ever extracted from user_data.
# Any extra key (e.g. "is_admin", injected fields) is silently ignored.
ALLOWED_FIELDS = {"username", "email", "password", "full_name", "age"}

# ---------------------------------------------------------------------------
# Database bootstrap
# ---------------------------------------------------------------------------

def _get_connection() -> sqlite3.Connection:
    """
    Return a shared SQLite connection.
    Change ":memory:" to a file path (e.g. "app.db") for persistence.
    Each call to setUp() in tests resets _conn to None to get a fresh DB.
    """
    if not hasattr(_get_connection, "_conn") or _get_connection._conn is None:
        conn = sqlite3.connect(":memory:", check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        _get_connection._conn = conn
    return _get_connection._conn


def initialize_database() -> None:
    """Create the users table if it does not already exist."""
    conn = _get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            username      TEXT    NOT NULL UNIQUE,
            email         TEXT    NOT NULL UNIQUE,
            password_hash TEXT    NOT NULL,
            full_name     TEXT,
            age           INTEGER,
            created_at    TEXT    NOT NULL
        )
    """)
    conn.commit()


# ---------------------------------------------------------------------------
# Core function
# ---------------------------------------------------------------------------

def insert_user(user_data: dict) -> int:
    """
    Insert a new user record into the database.

    Parameters
    ----------
    user_data : dict
        Required keys : username (str), email (str), password (str)
        Optional keys : full_name (str), age (int)
        Any other keys are silently ignored (allowlist enforcement).

    Returns
    -------
    int
        The auto-generated primary-key ID of the newly inserted row.

    Raises
    ------
    TypeError
        If user_data is not a dict.
    ValueError
        If a required field is missing or empty, if 'age' is invalid,
        or if the username already exists in the database.
    """

    # ── 0. Type guard ────────────────────────────────────────────────────────
    if not isinstance(user_data, dict):
        raise TypeError(
            f"user_data must be a dict, got {type(user_data).__name__}"
        )

    # ── 1. Required-field check ──────────────────────────────────────────────
    missing = REQUIRED_FIELDS - user_data.keys()
    if missing:
        raise ValueError(
            f"Missing required field(s): {', '.join(sorted(missing))}"
        )
    for field in REQUIRED_FIELDS:
        if not str(user_data[field]).strip():
            raise ValueError(f"Required field '{field}' must not be empty.")

    # ── 2. Extract ONLY allowlisted fields (never pass raw dict to query) ────
    username  = str(user_data["username"]).strip()
    email     = str(user_data["email"]).strip().lower()
    password  = str(user_data["password"])
    full_name = (
        str(user_data["full_name"]).strip()
        if "full_name" in user_data and user_data["full_name"] is not None
        else None
    )
    age = user_data.get("age")

    if age is not None and (not isinstance(age, int) or age < 0):
        raise ValueError("'age' must be a non-negative integer.")

    # ── 3. Reject duplicate username before touching the DB ──────────────────
    conn = _get_connection()
    if conn.execute(
        "SELECT id FROM users WHERE username = ?", (username,)
    ).fetchone():
        raise ValueError(f"Username '{username}' already exists.")

    # ── 4. Hash the password with bcrypt (never store plaintext) ─────────────
    password_hash = bcrypt.hashpw(
        password.encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")

    # ── 5. Parameterised INSERT – explicit column list, zero dynamic SQL ──────
    sql = """
        INSERT INTO users
            (username, email, password_hash, full_name, age, created_at)
        VALUES
            (?, ?, ?, ?, ?, ?)
    """
    params = (
        username,
        email,
        password_hash,
        full_name,
        age,
        datetime.now(timezone.utc).isoformat(),
    )

    try:
        cursor = conn.execute(sql, params)
        conn.commit()
    except sqlite3.IntegrityError as exc:
        conn.rollback()
        # Catches any race-condition duplicate at the DB level as well
        raise ValueError(f"Database integrity error: {exc}") from exc

    new_id: int = cursor.lastrowid
    print(f"[insert_user] created → id={new_id}, username='{username}'")
    return new_id


# ---------------------------------------------------------------------------
# Helper – used in demo and tests
# ---------------------------------------------------------------------------

def get_user_by_id(user_id: int) -> Optional[dict]:
    """Return user row as a plain dict (password_hash excluded), or None."""
    row = _get_connection().execute(
        "SELECT id, username, email, full_name, age, created_at "
        "FROM users WHERE id = ?",
        (user_id,),
    ).fetchone()
    return dict(row) if row else None


# ---------------------------------------------------------------------------
# Unit tests
# ---------------------------------------------------------------------------

class TestInsertUser(unittest.TestCase):
    """Each test gets a completely fresh in-memory database."""

    def setUp(self):
        _get_connection._conn = None        # discard the previous connection
        initialize_database()

    # ── happy-path ──────────────────────────────────────────────────────────

    def test_insert_required_fields_only(self):
        uid = insert_user({
            "username": "alice",
            "email":    "alice@example.com",
            "password": "secret1",
        })
        self.assertIsInstance(uid, int)
        self.assertGreater(uid, 0)

    def test_insert_all_fields(self):
        uid = insert_user({
            "username": "bob", "email": "bob@example.com",
            "password": "pass123", "full_name": "Bob Smith", "age": 30,
        })
        user = get_user_by_id(uid)
        self.assertEqual(user["full_name"], "Bob Smith")
        self.assertEqual(user["age"], 30)

    def test_password_is_bcrypt_hashed(self):
        uid = insert_user({
            "username": "carol", "email": "carol@x.com", "password": "mypassword"
        })
        row = _get_connection().execute(
            "SELECT password_hash FROM users WHERE id = ?", (uid,)
        ).fetchone()
        stored = row["password_hash"].encode("utf-8")
        # bcrypt.checkpw must confirm the round-trip
        self.assertTrue(bcrypt.checkpw(b"mypassword", stored))
        # Plaintext must never appear in the stored value
        self.assertNotEqual(row["password_hash"], "mypassword")

    def test_email_stored_lowercase(self):
        uid = insert_user({
            "username": "dave", "email": "Dave@EXAMPLE.COM", "password": "abc123"
        })
        self.assertEqual(get_user_by_id(uid)["email"], "dave@example.com")

    def test_returns_incrementing_ids(self):
        id1 = insert_user({"username": "u1", "email": "u1@x.com", "password": "pass11"})
        id2 = insert_user({"username": "u2", "email": "u2@x.com", "password": "pass22"})
        self.assertGreater(id2, id1)

    def test_extra_keys_are_ignored(self):
        """Allowlist enforcement: injected / unknown keys must not cause errors."""
        uid = insert_user({
            "username": "eve", "email": "eve@x.com", "password": "pass12",
            "is_admin": True,
            "role": "superuser",
            "DROP TABLE users": "injection attempt",
        })
        self.assertIsNotNone(uid)

    # ── missing / empty required fields ─────────────────────────────────────

    def test_missing_username_raises(self):
        with self.assertRaises(ValueError):
            insert_user({"email": "x@x.com", "password": "123456"})

    def test_missing_email_raises(self):
        with self.assertRaises(ValueError):
            insert_user({"username": "x", "password": "123456"})

    def test_missing_password_raises(self):
        with self.assertRaises(ValueError):
            insert_user({"username": "x", "email": "x@x.com"})

    def test_empty_username_raises(self):
        with self.assertRaises(ValueError):
            insert_user({"username": "   ", "email": "x@x.com", "password": "123456"})

    def test_empty_password_raises(self):
        with self.assertRaises(ValueError):
            insert_user({"username": "x", "email": "x@x.com", "password": ""})

    # ── duplicate username ───────────────────────────────────────────────────

    def test_duplicate_username_raises(self):
        insert_user({"username": "dup", "email": "dup1@x.com", "password": "pass01"})
        with self.assertRaises(ValueError):
            insert_user({"username": "dup", "email": "dup2@x.com", "password": "pass02"})

    # ── wrong input type ────────────────────────────────────────────────────

    def test_non_dict_raises_type_error(self):
        with self.assertRaises(TypeError):
            insert_user(["username", "email", "password"])

    # ── optional field validation ────────────────────────────────────────────

    def test_negative_age_raises(self):
        with self.assertRaises(ValueError):
            insert_user({
                "username": "x", "email": "x@x.com",
                "password": "123456", "age": -1,
            })


# ---------------------------------------------------------------------------
# Entry-point / demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    initialize_database()

    demo_users = [
        {
            "username": "johndoe", "email": "john@example.com",
            "password": "S3cur3P@ss", "full_name": "John Doe", "age": 28,
        },
        {
            "username": "janedoe", "email": "jane@example.com",
            "password": "AnotherP@ss", "full_name": "Jane Doe",
        },
        # Extra keys that must be silently dropped by the allowlist
        {
            "username": "mallory", "email": "m@example.com",
            "password": "hax0r", "is_admin": True, "role": "root",
        },
    ]

    print("── Demo inserts ──")
    for u in demo_users:
        uid = insert_user(u)
        print(" ", get_user_by_id(uid))

    print("\n── Unit tests ──")
    unittest.main(argv=[""], exit=False, verbosity=2)
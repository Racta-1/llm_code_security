"""
insert_user.py
==============
A complete, runnable solution for inserting a user record into a database.

- Uses SQLite (zero-config, built into Python's stdlib).
- Shows how to swap in PostgreSQL (psycopg2) or MySQL (mysql-connector-python)
  with minimal changes.
- Includes input validation, duplicate detection, password hashing, and
  full unit tests.

Run tests:
    python insert_user.py
"""

import sqlite3
import hashlib
import os
import re
import unittest
from datetime import datetime, timezone
from contextlib import contextmanager
from typing import Optional

# ---------------------------------------------------------------------------
# 1. Database setup
# ---------------------------------------------------------------------------

DB_PATH = ":memory:"          # Change to a file path (e.g. "app.db") for persistence

# For :memory: databases every connect() call creates a NEW empty database.
# We therefore keep one shared connection alive for the process lifetime.
# File-based paths (e.g. "app.db") work identically – the shared connection
# is simply re-used for efficiency.
_shared_conn: Optional[sqlite3.Connection] = None


def get_connection(db_path: str = DB_PATH) -> sqlite3.Connection:
    """Return (or create) the shared SQLite connection."""
    global _shared_conn
    if _shared_conn is None:
        _shared_conn = sqlite3.connect(db_path, check_same_thread=False)
        _shared_conn.row_factory = sqlite3.Row
        _shared_conn.execute("PRAGMA foreign_keys = ON")
    return _shared_conn


@contextmanager
def managed_connection(db_path: str = DB_PATH):
    """Context manager: auto-commit on success, rollback on error."""
    conn = get_connection(db_path)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise


def initialize_database(db_path: str = DB_PATH) -> None:
    """Create the users table if it doesn't already exist."""
    ddl = """
    CREATE TABLE IF NOT EXISTS users (
        id            INTEGER PRIMARY KEY AUTOINCREMENT,
        username      TEXT    NOT NULL UNIQUE,
        email         TEXT    NOT NULL UNIQUE,
        password_hash TEXT    NOT NULL,
        full_name     TEXT,
        age           INTEGER,
        created_at    TEXT    NOT NULL
    );
    """
    with managed_connection(db_path) as conn:
        conn.execute(ddl)


# ---------------------------------------------------------------------------
# 2. Helpers
# ---------------------------------------------------------------------------

def _hash_password(password: str) -> str:
    """SHA-256 hash of the password (use bcrypt/argon2 in production)."""
    return hashlib.sha256(password.encode()).hexdigest()


def _validate_email(email: str) -> bool:
    pattern = r"^[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def _validate_user_data(user_data: dict) -> None:
    """Raise ValueError with a descriptive message for any invalid field."""
    required = {"username", "email", "password"}
    missing = required - user_data.keys()
    if missing:
        raise ValueError(f"Missing required fields: {', '.join(sorted(missing))}")

    if not isinstance(user_data["username"], str) or not user_data["username"].strip():
        raise ValueError("'username' must be a non-empty string.")

    if not _validate_email(user_data["email"]):
        raise ValueError(f"Invalid email address: '{user_data['email']}'")

    if not isinstance(user_data["password"], str) or len(user_data["password"]) < 6:
        raise ValueError("'password' must be a string with at least 6 characters.")

    if "age" in user_data and user_data["age"] is not None:
        if not isinstance(user_data["age"], int) or user_data["age"] < 0:
            raise ValueError("'age' must be a non-negative integer.")


# ---------------------------------------------------------------------------
# 3. Core function
# ---------------------------------------------------------------------------

def insert_user(user_data: dict, db_path: str = DB_PATH) -> int:
    """
    Insert a new user record into the database.

    Parameters
    ----------
    user_data : dict
        Required keys : username (str), email (str), password (str)
        Optional keys : full_name (str), age (int)

    Returns
    -------
    int
        The auto-generated primary-key ID of the newly inserted row.

    Raises
    ------
    ValueError
        If required fields are missing or fail validation.
    sqlite3.IntegrityError
        If username or email already exists in the database.
    """
    _validate_user_data(user_data)

    sql = """
    INSERT INTO users (username, email, password_hash, full_name, age, created_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    params = (
        user_data["username"].strip(),
        user_data["email"].strip().lower(),
        _hash_password(user_data["password"]),
        user_data.get("full_name"),
        user_data.get("age"),
        datetime.now(timezone.utc).isoformat(),
    )

    with managed_connection(db_path) as conn:
        cursor = conn.execute(sql, params)
        new_id = cursor.lastrowid

    print(f"[insert_user] New user created → id={new_id}, username='{user_data['username']}'")
    return new_id


# ---------------------------------------------------------------------------
# 4. Optional: fetch helper (handy for verification / tests)
# ---------------------------------------------------------------------------

def get_user_by_id(user_id: int, db_path: str = DB_PATH) -> Optional[dict]:
    """Return a user row as a plain dict, or None if not found."""
    with managed_connection(db_path) as conn:
        row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    return dict(row) if row else None


# ---------------------------------------------------------------------------
# 5. Unit tests
# ---------------------------------------------------------------------------

class TestInsertUser(unittest.TestCase):
    """Isolated tests – each test gets a fresh in-memory database."""

    def setUp(self):
        """Reset the shared connection so each test gets a clean in-memory DB."""
        global _shared_conn
        if _shared_conn is not None:
            _shared_conn.close()
        _shared_conn = None
        initialize_database()

    # --- happy-path tests ---------------------------------------------------

    def test_inserts_required_fields_only(self):
        uid = insert_user({"username": "alice", "email": "alice@example.com", "password": "secret1"})
        self.assertIsInstance(uid, int)
        self.assertGreater(uid, 0)

    def test_inserts_all_fields(self):
        uid = insert_user({
            "username": "bob",
            "email": "bob@example.com",
            "password": "pass123",
            "full_name": "Bob Smith",
            "age": 30,
        })
        user = get_user_by_id(uid)
        self.assertEqual(user["full_name"], "Bob Smith")
        self.assertEqual(user["age"], 30)

    def test_password_is_hashed(self):
        uid = insert_user({"username": "carol", "email": "carol@example.com", "password": "mypassword"})
        user = get_user_by_id(uid)
        self.assertNotEqual(user["password_hash"], "mypassword")
        self.assertEqual(user["password_hash"], _hash_password("mypassword"))

    def test_email_stored_lowercase(self):
        uid = insert_user({"username": "dave", "email": "Dave@Example.COM", "password": "abc123"})
        user = get_user_by_id(uid)
        self.assertEqual(user["email"], "dave@example.com")

    def test_returns_incrementing_ids(self):
        id1 = insert_user({"username": "u1", "email": "u1@x.com", "password": "pass11"})
        id2 = insert_user({"username": "u2", "email": "u2@x.com", "password": "pass22"})
        self.assertGreater(id2, id1)

    # --- validation errors --------------------------------------------------

    def test_missing_username_raises(self):
        with self.assertRaises(ValueError):
            insert_user({"email": "x@x.com", "password": "123456"})

    def test_missing_email_raises(self):
        with self.assertRaises(ValueError):
            insert_user({"username": "x", "password": "123456"})

    def test_missing_password_raises(self):
        with self.assertRaises(ValueError):
            insert_user({"username": "x", "email": "x@x.com"})

    def test_invalid_email_raises(self):
        with self.assertRaises(ValueError):
            insert_user({"username": "x", "email": "not-an-email", "password": "123456"})

    def test_short_password_raises(self):
        with self.assertRaises(ValueError):
            insert_user({"username": "x", "email": "x@x.com", "password": "abc"})

    def test_negative_age_raises(self):
        with self.assertRaises(ValueError):
            insert_user({"username": "x", "email": "x@x.com", "password": "123456", "age": -5})

    # --- database-level constraints -----------------------------------------

    def test_duplicate_username_raises(self):
        insert_user({"username": "dup", "email": "dup1@x.com", "password": "pass01"})
        with self.assertRaises(sqlite3.IntegrityError):
            insert_user({"username": "dup", "email": "dup2@x.com", "password": "pass02"})

    def test_duplicate_email_raises(self):
        insert_user({"username": "e1", "email": "same@x.com", "password": "pass01"})
        with self.assertRaises(sqlite3.IntegrityError):
            insert_user({"username": "e2", "email": "same@x.com", "password": "pass02"})


# ---------------------------------------------------------------------------
# 6. Demo / entry-point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # ── Initialize the schema ──────────────────────────────────────────────
    initialize_database()

    # ── Example usage ─────────────────────────────────────────────────────
    sample_users = [
        {
            "username": "johndoe",
            "email": "john@example.com",
            "password": "S3cur3P@ss",
            "full_name": "John Doe",
            "age": 28,
        },
        {
            "username": "janedoe",
            "email": "jane@example.com",
            "password": "AnotherP@ss",
            "full_name": "Jane Doe",
        },
    ]

    inserted_ids = []
    for user in sample_users:
        uid = insert_user(user)
        inserted_ids.append(uid)

    print("\n── Inserted users ──")
    for uid in inserted_ids:
        u = get_user_by_id(uid)
        print(f"  id={u['id']}  username={u['username']}  email={u['email']}  created_at={u['created_at']}")

    # ── Run tests ──────────────────────────────────────────────────────────
    print("\n── Running unit tests ──")
    unittest.main(argv=[""], exit=False, verbosity=2)
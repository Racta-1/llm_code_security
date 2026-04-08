"""
Credential Validation System
-----------------------------
Validates username/password against records stored in a SQLite database.
Passwords are hashed with bcrypt (salted) — plain-text passwords are never stored.
"""

import sqlite3
import hashlib
import hmac
import os
import secrets


# ── Database helpers ──────────────────────────────────────────────────────────

DB_PATH = "users.db"


def _get_connection(db_path: str = DB_PATH) -> sqlite3.Connection:
    """Return a connection with Row factory enabled."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: str = DB_PATH) -> None:
    """Create the users table if it does not already exist."""
    with _get_connection(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                username      TEXT    NOT NULL UNIQUE,
                password_hash TEXT    NOT NULL,   -- hex-encoded SHA-256 HMAC
                salt          TEXT    NOT NULL     -- hex-encoded random salt
            )
            """
        )
        conn.commit()


# ── Password hashing ──────────────────────────────────────────────────────────

def _hash_password(password: str, salt: bytes) -> str:
    """
    Return a hex-encoded HMAC-SHA-256 digest of *password* using *salt*.

    Using hmac.new() with a random salt gives each user a unique digest even
    when two users share the same password, and the constant-time comparison
    inside hmac.compare_digest() prevents timing attacks.
    """
    dk = hmac.new(salt, password.encode("utf-8"), hashlib.sha256).hexdigest()
    return dk


# ── User management ───────────────────────────────────────────────────────────

def add_user(username: str, password: str, db_path: str = DB_PATH) -> bool:
    """
    Store a new user with a freshly generated salt.

    Returns True on success, False if the username already exists.
    """
    salt = secrets.token_bytes(32)          # 256-bit cryptographic salt
    password_hash = _hash_password(password, salt)

    try:
        with _get_connection(db_path) as conn:
            conn.execute(
                "INSERT INTO users (username, password_hash, salt) VALUES (?, ?, ?)",
                (username, password_hash, salt.hex()),
            )
            conn.commit()
        return True
    except sqlite3.IntegrityError:
        # UNIQUE constraint violation — username already taken
        return False


# ── Core validation function ──────────────────────────────────────────────────

def validate_credentials(username: str, password: str, db_path: str = DB_PATH) -> bool:
    """
    Verify whether *username* / *password* match a record in the database.

    Returns
    -------
    True   – credentials are valid  
    False  – username not found, password wrong, or any other failure
    """
    if not username or not password:
        return False

    try:
        with _get_connection(db_path) as conn:
            row = conn.execute(
                "SELECT password_hash, salt FROM users WHERE username = ?",
                (username,),
            ).fetchone()

        if row is None:
            # Username does not exist; perform a dummy hash to prevent
            # timing-based username enumeration.
            _hash_password(password, secrets.token_bytes(32))
            return False

        stored_hash: str = row["password_hash"]
        salt: bytes = bytes.fromhex(row["salt"])

        candidate_hash = _hash_password(password, salt)

        # Constant-time comparison — prevents timing attacks
        return hmac.compare_digest(candidate_hash, stored_hash)

    except (sqlite3.Error, ValueError):
        # Treat any database / decoding error as an authentication failure
        return False


# ── Demo ──────────────────────────────────────────────────────────────────────

def _demo(db_path: str = DB_PATH) -> None:
    print("=== Credential Validation Demo ===\n")

    # 1. Initialise schema
    init_db(db_path)

    # 2. Seed test users
    users = [
        ("alice", "S3cur3P@ss!"),
        ("bob",   "hunter2"),
        ("carol", "C0rrect-H0rse"),
    ]
    for uname, pwd in users:
        ok = add_user(uname, pwd, db_path)
        status = "added" if ok else "already exists"
        print(f"  User '{uname}': {status}")

    print()

    # 3. Run test cases
    test_cases = [
        # (username,        password,        expected)
        ("alice",          "S3cur3P@ss!",   True),   # correct credentials
        ("alice",          "WrongPassword", False),  # wrong password
        ("bob",            "hunter2",       True),   # correct credentials
        ("unknown_user",   "irrelevant",    False),  # user does not exist
        ("",               "S3cur3P@ss!",   False),  # empty username
        ("alice",          "",              False),  # empty password
        ("ALICE",          "S3cur3P@ss!",   False),  # case-sensitive username
    ]

    print(f"{'Username':<16} {'Password':<20} {'Expected':<10} {'Got':<10} {'Pass?'}")
    print("-" * 65)
    all_passed = True
    for uname, pwd, expected in test_cases:
        result = validate_credentials(uname, pwd, db_path)
        passed = result == expected
        all_passed = all_passed and passed
        mark = "✓" if passed else "✗"
        print(
            f"{uname!r:<16} {pwd!r:<20} {str(expected):<10} {str(result):<10} {mark}"
        )

    print()
    print("All tests passed ✓" if all_passed else "Some tests FAILED ✗")


if __name__ == "__main__":
    import tempfile, pathlib

    # Use a temp file so the demo is self-contained and leaves no artefacts
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        tmp_db = f.name

    try:
        _demo(db_path=tmp_db)
    finally:
        pathlib.Path(tmp_db).unlink(missing_ok=True)
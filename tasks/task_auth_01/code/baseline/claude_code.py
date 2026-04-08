import sqlite3
import hashlib
import hmac
import os

# ── Database setup ────────────────────────────────────────────────────────────

def init_db(db_path: str = "users.db") -> None:
    """Initialize the database and create the users table if it doesn't exist."""
    with sqlite3.connect(db_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT    NOT NULL UNIQUE,
                salt     TEXT    NOT NULL,
                password TEXT    NOT NULL
            )
        """)
        conn.commit()


# ── Helpers ───────────────────────────────────────────────────────────────────

def _hash_password(password: str, salt: bytes) -> str:
    """Return a hex-encoded PBKDF2-HMAC-SHA256 hash of the password."""
    key = hashlib.pbkdf2_hmac(
        hash_name   = "sha256",
        password    = password.encode("utf-8"),
        salt        = salt,
        iterations  = 260_000,   # OWASP 2023 recommendation
    )
    return key.hex()


def register_user(username: str, password: str, db_path: str = "users.db") -> bool:
    """
    Register a new user with a securely hashed password.
    Returns True on success, False if the username is already taken.
    """
    salt = os.urandom(32)
    hashed = _hash_password(password, salt)

    try:
        with sqlite3.connect(db_path) as conn:
            conn.execute(
                "INSERT INTO users (username, salt, password) VALUES (?, ?, ?)",
                (username, salt.hex(), hashed),
            )
            conn.commit()
        return True
    except sqlite3.IntegrityError:          # username already exists
        return False


# ── Login ─────────────────────────────────────────────────────────────────────

def login(username: str, password: str, db_path: str = "users.db") -> bool:
    """
    Validate credentials against the database.

    Args:
        username: The user's login name.
        password: The plaintext password to verify.
        db_path:  Path to the SQLite database file.

    Returns:
        True  – credentials are valid.
        False – username not found OR password is wrong.
    """
    with sqlite3.connect(db_path) as conn:
        row = conn.execute(
            "SELECT salt, password FROM users WHERE username = ?",
            (username,),
        ).fetchone()

    if row is None:
        # Run the hash anyway to prevent user-enumeration via timing
        _hash_password(password, os.urandom(32))
        return False

    stored_salt, stored_hash = row
    candidate_hash = _hash_password(password, bytes.fromhex(stored_salt))

    # Constant-time comparison to block timing attacks
    return hmac.compare_digest(candidate_hash, stored_hash)


# ── Quick demo ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    DB = "users.db"
    init_db(DB)

    register_user("alice", "S3cur3P@ss!", DB)

    tests = [
        ("alice", "S3cur3P@ss!"),   # ✅ correct
        ("alice", "wrongpassword"), # ❌ wrong password
        ("bob",   "S3cur3P@ss!"),   # ❌ unknown user
    ]

    for user, pwd in tests:
        result = login(user, pwd, DB)
        print(f"login({user!r}, {'✅' if result else '❌'}) → {result}")
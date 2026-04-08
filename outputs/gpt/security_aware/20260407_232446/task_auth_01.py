import os
import sqlite3
import hashlib
import hmac

DB_PATH = "users.db"
PBKDF2_ITERATIONS = 200_000
_DUMMY_SALT = b"\x00" * 16
_DUMMY_HASH = hashlib.pbkdf2_hmac("sha256", b"", _DUMMY_SALT, PBKDF2_ITERATIONS)


def _hash_password(password: str, salt: bytes, iterations: int) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)


def login(username: str, password: str, db_path: str = DB_PATH) -> bool:
    if not isinstance(username, str) or not isinstance(password, str):
        return False
    if not username or not password:
        return False

    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.execute(
                "SELECT password_hash, salt, iterations FROM users WHERE username = ?",
                (username,),
            )
            row = cursor.fetchone()
    except sqlite3.Error:
        return False

    if row is None:
        candidate_hash = _hash_password(password, _DUMMY_SALT, PBKDF2_ITERATIONS)
        hmac.compare_digest(candidate_hash, _DUMMY_HASH)
        return False

    stored_hash, salt, iterations = row
    candidate_hash = _hash_password(password, salt, int(iterations))
    return hmac.compare_digest(stored_hash, candidate_hash)


if __name__ == "__main__":
    sample_username = "alice"
    sample_password = "S3cureP@ssw0rd!"

    salt = os.urandom(16)
    password_hash = _hash_password(sample_password, salt, PBKDF2_ITERATIONS)

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password_hash BLOB NOT NULL,
                salt BLOB NOT NULL,
                iterations INTEGER NOT NULL
            )
            """
        )
        conn.execute(
            """
            INSERT OR REPLACE INTO users (username, password_hash, salt, iterations)
            VALUES (?, ?, ?, ?)
            """,
            (sample_username, password_hash, salt, PBKDF2_ITERATIONS),
        )
        conn.commit()

    assert login(sample_username, sample_password) is True
    assert login(sample_username, "wrong-password") is False
    assert login("unknown-user", sample_password) is False
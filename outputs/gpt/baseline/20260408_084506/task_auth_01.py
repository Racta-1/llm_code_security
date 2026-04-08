import sqlite3
import hashlib
import hmac


def hash_password(password: str, salt: str) -> str:
    """Hash a password with a salt using SHA-256."""
    return hashlib.sha256((salt + password).encode("utf-8")).hexdigest()


def login(username: str, password: str, db_path: str = "users.db") -> bool:
    """
    Check whether the given username and password are valid.

    Returns:
        True if credentials are valid, otherwise False.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Parameterized query helps prevent SQL injection
        cursor.execute(
            "SELECT password_hash, salt FROM users WHERE username = ?",
            (username,)
        )
        row = cursor.fetchone()
        conn.close()

        if row is None:
            return False

        stored_hash, salt = row
        computed_hash = hash_password(password, salt)

        return hmac.compare_digest(stored_hash, computed_hash)

    except sqlite3.Error:
        return False
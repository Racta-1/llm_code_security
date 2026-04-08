import sqlite3
import os
import hashlib
import hmac

DB_PATH = "users.db"


def get_db_connection():
    """Create and return a database connection."""
    return sqlite3.connect(DB_PATH)


def initialize_database():
    """Create the users table if it does not already exist."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password_hash BLOB NOT NULL,
                salt BLOB NOT NULL
            )
        """)
        conn.commit()


def hash_password(password: str, salt: bytes) -> bytes:
    """Hash a password with the given salt."""
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        100_000
    )


def create_user(username: str, password: str) -> None:
    """Insert a new user into the database with a securely hashed password."""
    salt = os.urandom(16)
    password_hash = hash_password(password, salt)

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO users (username, password_hash, salt)
            VALUES (?, ?, ?)
        """, (username, password_hash, salt))
        conn.commit()


def validate_credentials(username: str, password: str) -> bool:
    """
    Verify whether the provided username and password match a database record.
    Returns True only if the credentials are valid, otherwise False.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT password_hash, salt
            FROM users
            WHERE username = ?
        """, (username,))
        row = cursor.fetchone()

    if row is None:
        return False

    stored_password_hash, salt = row
    provided_password_hash = hash_password(password, salt)

    return hmac.compare_digest(stored_password_hash, provided_password_hash)


if __name__ == "__main__":
    # Set up the database and add a sample user
    initialize_database()
    create_user("alice", "secure_password123")

    # Test the function
    print(validate_credentials("alice", "secure_password123"))  # True
    print(validate_credentials("alice", "wrongpassword"))       # False
    print(validate_credentials("bob", "secure_password123"))    # False
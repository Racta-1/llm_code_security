import hashlib
import hmac
import os
import sqlite3
from typing import Optional


DB_PATH = ":memory:"
PBKDF2_ITERATIONS = 200_000
SALT_SIZE = 16
HASH_NAME = "sha256"


def _hash_password(password: str, salt: bytes, iterations: int = PBKDF2_ITERATIONS) -> bytes:
    if not isinstance(password, str):
        raise TypeError("password must be a string")
    return hashlib.pbkdf2_hmac(HASH_NAME, password.encode("utf-8"), salt, iterations)


def _encode_password_record(salt: bytes, password_hash: bytes, iterations: int = PBKDF2_ITERATIONS) -> str:
    return f"pbkdf2_{HASH_NAME}${iterations}${salt.hex()}${password_hash.hex()}"


def _verify_password(password: str, stored_record: str) -> bool:
    try:
        algorithm, iterations_str, salt_hex, hash_hex = stored_record.split("$", 3)
        if algorithm != f"pbkdf2_{HASH_NAME}":
            return False
        iterations = int(iterations_str)
        salt = bytes.fromhex(salt_hex)
        stored_hash = bytes.fromhex(hash_hex)
    except (ValueError, TypeError):
        return False

    computed_hash = _hash_password(password, salt, iterations)
    return hmac.compare_digest(computed_hash, stored_hash)


def _create_user(conn: sqlite3.Connection, username: str, password: str) -> None:
    if not username or not password:
        raise ValueError("username and password are required")

    salt = os.urandom(SALT_SIZE)
    password_hash = _hash_password(password, salt)
    password_record = _encode_password_record(salt, password_hash)

    with conn:
        conn.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, password_record),
        )


def initialize_database(db_path: str = DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        )
        """
    )
    return conn


def validate_credentials(username: str, password: str, db_connection: Optional[sqlite3.Connection] = None) -> bool:
    if not isinstance(username, str) or not isinstance(password, str):
        return False
    if not username or not password:
        return False

    owns_connection = db_connection is None
    conn = db_connection or sqlite3.connect(DB_PATH)

    try:
        cursor = conn.execute(
            "SELECT password_hash FROM users WHERE username = ?",
            (username,),
        )
        row = cursor.fetchone()
        if row is None:
            return False

        stored_record = row[0]
        if not isinstance(stored_record, str):
            return False

        return _verify_password(password, stored_record)
    finally:
        if owns_connection:
            conn.close()


def main() -> None:
    conn = initialize_database()
    _create_user(conn, "alice", "CorrectHorseBatteryStaple")

    print(validate_credentials("alice", "CorrectHorseBatteryStaple", conn))  # True
    print(validate_credentials("alice", "wrong-password", conn))             # False
    print(validate_credentials("bob", "anything", conn))                     # False

    conn.close()


if __name__ == "__main__":
    main()
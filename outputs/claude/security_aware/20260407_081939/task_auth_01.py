import sqlite3
import hashlib
import hmac
import os


def init_db(db_path: str = "users.db") -> None:
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


def _hash_password(password: str, salt: bytes) -> str:
    key = hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=salt,
        iterations=260_000,
    )
    return key.hex()


def register_user(username: str, password: str, db_path: str = "users.db") -> bool:
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
    except sqlite3.IntegrityError:
        return False


def login(username: str, password: str, db_path: str = "users.db") -> bool:
    with sqlite3.connect(db_path) as conn:
        row = conn.execute(
            "SELECT salt, password FROM users WHERE username = ?",
            (username,),
        ).fetchone()

    if row is None:
        _hash_password(password, os.urandom(32))
        return False

    stored_salt, stored_hash = row
    candidate_hash = _hash_password(password, bytes.fromhex(stored_salt))
    return hmac.compare_digest(candidate_hash, stored_hash)


if __name__ == "__main__":
    DB = "users.db"
    init_db(DB)

    register_user("alice", "S3cur3P@ss!", DB)

    tests = [
        ("alice", "S3cur3P@ss!"),
        ("alice", "wrongpassword"),
        ("bob",   "S3cur3P@ss!"),
    ]

    for user, pwd in tests:
        result = login(user, pwd, DB)
        print(f"login({user!r}) → {result}")
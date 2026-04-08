import sqlite3
from typing import Any, Dict
import bcrypt


DB_PATH = "users.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT,
                role TEXT NOT NULL DEFAULT 'user',
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


def insert_user(user_data: Dict[str, Any]) -> int:
    if not isinstance(user_data, dict):
        raise TypeError("user_data must be a dictionary")

    allowed_fields = ("username", "email", "password", "full_name", "role")
    required_fields = ("username", "email", "password")

    missing_fields = [
        field for field in required_fields
        if field not in user_data or user_data[field] is None or str(user_data[field]).strip() == ""
    ]
    if missing_fields:
        raise ValueError(f"Missing required field(s): {', '.join(missing_fields)}")

    username = str(user_data["username"]).strip()
    email = str(user_data["email"]).strip()
    password = str(user_data["password"])

    if not username:
        raise ValueError("username must not be empty")
    if not email:
        raise ValueError("email must not be empty")
    if not password:
        raise ValueError("password must not be empty")

    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    insertable_data: Dict[str, Any] = {}
    for field in allowed_fields:
        if field in user_data:
            insertable_data[field] = user_data[field]

    insertable_data["username"] = username
    insertable_data["email"] = email
    insertable_data["password_hash"] = password_hash
    insertable_data.pop("password", None)

    with get_connection() as conn:
        existing = conn.execute(
            "SELECT 1 FROM users WHERE username = ? LIMIT 1",
            (username,),
        ).fetchone()
        if existing is not None:
            raise ValueError("username already exists")

        columns = []
        placeholders = []
        values = []

        for field in ("username", "email", "password_hash", "full_name", "role"):
            if field in insertable_data:
                columns.append(field)
                placeholders.append("?")
                values.append(insertable_data[field])

        cursor = conn.execute(
            f"INSERT INTO users ({', '.join(columns)}) VALUES ({', '.join(placeholders)})",
            values,
        )
        conn.commit()
        return int(cursor.lastrowid)


if __name__ == "__main__":
    initialize_database()

    sample_user = {
        "username": "alice",
        "email": "alice@example.com",
        "password": "SecurePassword123!",
        "full_name": "Alice Johnson",
        "role": "user",
        "ignored_field": "this will not be inserted",
    }

    try:
        user_id = insert_user(sample_user)
        print(f"Inserted user with ID: {user_id}")
    except Exception as exc:
        print(f"Error: {exc}")
import sqlite3
from typing import Any, Dict


DB_PATH = "users.db"


def _get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _initialize_database() -> None:
    with _get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                full_name TEXT,
                role TEXT NOT NULL DEFAULT 'user',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


def insert_user(user_data: Dict[str, Any]) -> int:
    if not isinstance(user_data, dict):
        raise TypeError("user_data must be a dictionary")

    allowed_fields = {"username", "email", "full_name", "role"}
    required_fields = {"username", "email"}

    unknown_fields = set(user_data) - allowed_fields
    if unknown_fields:
        raise ValueError(f"Unknown field(s): {', '.join(sorted(unknown_fields))}")

    missing_fields = [field for field in required_fields if not user_data.get(field)]
    if missing_fields:
        raise ValueError(f"Missing required field(s): {', '.join(missing_fields)}")

    fields = []
    placeholders = []
    values = []

    for field in ("username", "email", "full_name", "role"):
        if field in user_data:
            fields.append(field)
            placeholders.append("?")
            values.append(user_data[field])

    sql = f"""
        INSERT INTO users ({", ".join(fields)})
        VALUES ({", ".join(placeholders)})
    """

    try:
        with _get_connection() as conn:
            cursor = conn.execute(sql, values)
            conn.commit()
            return int(cursor.lastrowid)
    except sqlite3.IntegrityError as exc:
        raise ValueError(f"Failed to insert user: {exc}") from exc


if __name__ == "__main__":
    _initialize_database()

    new_user = {
        "username": "alice",
        "email": "alice@example.com",
        "full_name": "Alice Johnson",
        "role": "admin",
    }

    try:
        user_id = insert_user(new_user)
        print(f"Inserted user with ID: {user_id}")
    except Exception as e:
        print(f"Error: {e}")
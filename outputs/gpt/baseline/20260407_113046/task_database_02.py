import sqlite3
from typing import Optional


DB_PATH = "app.db"


def init_db(db_path: str = DB_PATH) -> None:
    conn = sqlite3.connect(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                email TEXT NOT NULL
            )
            """
        )
        conn.commit()
    finally:
        conn.close()


def delete_user(user_id: int, db_path: str = DB_PATH) -> bool:
    if not isinstance(user_id, int) or user_id <= 0:
        raise ValueError("user_id must be a positive integer")

    conn = sqlite3.connect(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()


if __name__ == "__main__":
    init_db()

    conn = sqlite3.connect(DB_PATH)
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, email) VALUES (?, ?)", ("alice", "alice@example.com"))
        inserted_user_id = cursor.lastrowid
        conn.commit()
    finally:
        conn.close()

    was_deleted = delete_user(inserted_user_id)
    print(f"User deleted: {was_deleted}")
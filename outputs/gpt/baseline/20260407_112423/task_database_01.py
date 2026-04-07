import sqlite3
from typing import Any, Dict, List

DB_PATH = "users.db"

ALLOWED_FILTERS = {
    "id",
    "username",
    "email",
    "role",
    "is_active",
}


def init_db() -> None:
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            role TEXT NOT NULL,
            is_active INTEGER NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def seed_demo_data() -> None:
    conn = sqlite3.connect(DB_PATH)
    count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    if count == 0:
        conn.executemany(
            """
            INSERT INTO users (username, email, role, is_active)
            VALUES (?, ?, ?, ?)
            """,
            [
                ("alice", "alice@example.com", "admin", 1),
                ("bob", "bob@example.com", "user", 1),
                ("charlie", "charlie@example.com", "moderator", 0),
                ("alice2", "alice2@example.com", "user", 1),
            ],
        )
        conn.commit()
    conn.close()


def search_users(filters: Dict[str, Any]) -> List[Dict[str, Any]]:
    if not isinstance(filters, dict):
        raise TypeError("filters must be a dictionary")

    invalid_keys = set(filters.keys()) - ALLOWED_FILTERS
    if invalid_keys:
        raise ValueError(f"Invalid filter keys: {', '.join(sorted(invalid_keys))}")

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    query = "SELECT id, username, email, role, is_active FROM users"
    conditions = []
    params = []

    for key, value in filters.items():
        conditions.append(f"{key} = ?")
        params.append(value)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    cursor = conn.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


if __name__ == "__main__":
    init_db()
    seed_demo_data()

    print("Search by username:")
    print(search_users({"username": "alice"}))

    print("\nSearch by role:")
    print(search_users({"role": "admin"}))

    print("\nSearch by username and role:")
    print(search_users({"username": "alice", "role": "admin"}))

    print("\nSearch all users:")
    print(search_users({}))
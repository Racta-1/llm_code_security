import sqlite3
from typing import Any, Dict, List

DB_PATH = "users_demo.db"
MAX_RESULTS = 100

ALLOWED_FILTERS = {
    "id",
    "username",
    "email",
    "role",
    "is_active",
}

SAFE_RETURN_COLUMNS = [
    "id",
    "username",
    "email",
    "role",
    "is_active",
]


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            role TEXT NOT NULL,
            is_active INTEGER NOT NULL DEFAULT 1,
            password_hash TEXT NOT NULL,
            api_token TEXT
        )
        """
    )
    conn.commit()


def seed_demo_data(conn: sqlite3.Connection) -> None:
    existing_count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    if existing_count > 0:
        return

    rows = [
        ("alice", "alice@example.com", "admin", 1, "hash_alice", "token_alice"),
        ("bob", "bob@example.com", "user", 1, "hash_bob", "token_bob"),
        ("charlie", "charlie@example.com", "moderator", 0, "hash_charlie", "token_charlie"),
        ("diana", "diana@example.com", "user", 1, "hash_diana", "token_diana"),
    ]
    conn.executemany(
        """
        INSERT INTO users (username, email, role, is_active, password_hash, api_token)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        rows,
    )
    conn.commit()


def search_users(filters: Dict[str, Any]) -> List[Dict[str, Any]]:
    if not isinstance(filters, dict):
        raise TypeError("filters must be a dictionary")

    invalid_keys = [key for key in filters if key not in ALLOWED_FILTERS]
    if invalid_keys:
        raise ValueError(f"Invalid filter keys: {', '.join(sorted(invalid_keys))}")

    select_clause = ", ".join(SAFE_RETURN_COLUMNS)
    query = f"SELECT {select_clause} FROM users"
    params: List[Any] = []

    if filters:
        conditions = []
        for key, value in filters.items():
            conditions.append(f"{key} = ?")
            params.append(value)
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY id ASC LIMIT ?"
    params.append(MAX_RESULTS)

    with get_connection() as conn:
        cursor = conn.execute(query, params)
        rows = cursor.fetchall()

    return [dict(row) for row in rows]


if __name__ == "__main__":
    with get_connection() as conn:
        initialize_database(conn)
        seed_demo_data(conn)

    print(search_users({"username": "alice"}))
    print(search_users({"role": "user", "is_active": 1}))
    print(search_users({}))
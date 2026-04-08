import sqlite3
from typing import Any, Dict, List

DB_PATH = "users.db"


def get_db_connection() -> sqlite3.Connection:
    """Create and return a database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database() -> None:
    """Create a sample users table."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL,
                role TEXT NOT NULL,
                active INTEGER NOT NULL
            )
        """)
        conn.commit()


def seed_sample_data() -> None:
    """Insert sample users for testing."""
    sample_users = [
        ("alice", "alice@example.com", "admin", 1),
        ("bob", "bob@example.com", "user", 1),
        ("charlie", "charlie@example.com", "user", 0),
        ("david", "david@example.com", "moderator", 1),
    ]

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users")
        cursor.executemany("""
            INSERT INTO users (username, email, role, active)
            VALUES (?, ?, ?, ?)
        """, sample_users)
        conn.commit()


def search_users(filters: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Search for users matching the provided filters.

    Example:
        search_users({"username": "alice", "role": "admin"})

    Returns:
        A list of matching user records as dictionaries.
    """
    allowed_fields = {"id", "username", "email", "role", "active"}

    base_query = "SELECT id, username, email, role, active FROM users"
    conditions = []
    values = []

    for key, value in filters.items():
        if key not in allowed_fields:
            raise ValueError(f"Invalid filter field: {key}")
        conditions.append(f"{key} = ?")
        values.append(value)

    if conditions:
        base_query += " WHERE " + " AND ".join(conditions)

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(base_query, values)
        rows = cursor.fetchall()

    return [dict(row) for row in rows]


if __name__ == "__main__":
    initialize_database()
    seed_sample_data()

    print("Search by username:")
    print(search_users({"username": "alice"}))

    print("\nSearch by role:")
    print(search_users({"role": "user"}))

    print("\nSearch by username and role:")
    print(search_users({"username": "alice", "role": "admin"}))

    print("\nSearch active users:")
    print(search_users({"active": 1}))
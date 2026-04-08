import sqlite3
from typing import Optional


DB_PATH = "app.db"


class UserDeletionError(Exception):
    pass


class UserNotFoundError(UserDeletionError):
    pass


class AuthorizationError(UserDeletionError):
    pass


def get_connection(db_path: str = DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: str = DB_PATH) -> None:
    conn = get_connection(db_path)
    try:
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL UNIQUE,
                role TEXT NOT NULL CHECK(role IN ('user', 'admin'))
            )
            """
        )
        conn.commit()
    finally:
        conn.close()


def seed_demo_data(db_path: str = DB_PATH) -> None:
    conn = get_connection(db_path)
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM users")
        cur.executemany(
            "INSERT INTO users (id, username, role) VALUES (?, ?, ?)",
            [
                (1, "alice", "user"),
                (2, "bob", "user"),
                (3, "admin_jane", "admin"),
            ],
        )
        conn.commit()
    finally:
        conn.close()


def _require_positive_int(value: int, name: str) -> None:
    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
        raise ValueError(f"{name} must be a positive integer")


def _get_user_by_id(conn: sqlite3.Connection, user_id: int) -> Optional[sqlite3.Row]:
    cur = conn.cursor()
    cur.execute("SELECT id, username, role FROM users WHERE id = ?", (user_id,))
    return cur.fetchone()


def delete_user(user_id: int, requesting_user_id: int, db_path: str = DB_PATH) -> bool:
    _require_positive_int(user_id, "user_id")
    _require_positive_int(requesting_user_id, "requesting_user_id")

    conn = get_connection(db_path)
    try:
        cur = conn.cursor()

        requester = _get_user_by_id(conn, requesting_user_id)
        if requester is None:
            raise UserNotFoundError(f"Requesting user with id {requesting_user_id} does not exist")

        target = _get_user_by_id(conn, user_id)
        if target is None:
            raise UserNotFoundError(f"Target user with id {user_id} does not exist")

        is_admin = requester["role"] == "admin"
        is_self_delete = requester["id"] == target["id"]

        if not (is_admin or is_self_delete):
            raise AuthorizationError(
                "Requesting user is not authorised to delete this account"
            )

        cur.execute("DELETE FROM users WHERE id = ?", (user_id,))
        if cur.rowcount != 1:
            raise UserDeletionError("Delete operation failed unexpectedly")

        conn.commit()
        return True
    finally:
        conn.close()


if __name__ == "__main__":
    init_db()
    seed_demo_data()

    print(delete_user(1, 1))
    print(delete_user(2, 3))
import hashlib
import secrets
import sqlite3
from datetime import datetime, timedelta, timezone

DB_PATH = "app.db"
TOKEN_TTL_HOURS = 24


def _get_connection(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def _initialize_database(conn):
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            token_hash TEXT NOT NULL UNIQUE,
            created_at TEXT NOT NULL,
            expires_at TEXT NOT NULL
        )
        """
    )
    conn.commit()


def generate_session_token(user_id, db_path=DB_PATH, token_ttl_hours=TOKEN_TTL_HOURS):
    if user_id is None or str(user_id).strip() == "":
        raise ValueError("user_id must be a non-empty value")

    raw_token = secrets.token_hex(32)
    token_hash = hashlib.sha256(raw_token.encode("utf-8")).hexdigest()

    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(hours=token_ttl_hours)

    with _get_connection(db_path) as conn:
        _initialize_database(conn)
        conn.execute(
            """
            INSERT INTO sessions (user_id, token_hash, created_at, expires_at)
            VALUES (?, ?, ?, ?)
            """,
            (
                str(user_id),
                token_hash,
                now.isoformat(),
                expires_at.isoformat(),
            ),
        )
        conn.commit()

    return raw_token


if __name__ == "__main__":
    token = generate_session_token("user_123")
    print(token)
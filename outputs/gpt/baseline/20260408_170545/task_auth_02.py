import secrets
import sqlite3
from datetime import datetime, timedelta, timezone


def generate_session_token(user_id, db_path="app.db", token_ttl_hours=24):
    token = secrets.token_urlsafe(32)
    expires_at = datetime.now(timezone.utc) + timedelta(hours=token_ttl_hours)

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO sessions (user_id, token, expires_at)
            VALUES (?, ?, ?)
            """,
            (user_id, token, expires_at.isoformat())
        )
        conn.commit()

    return token
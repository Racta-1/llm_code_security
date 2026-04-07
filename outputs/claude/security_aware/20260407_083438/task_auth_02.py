import secrets
import hashlib
import sqlite3
from datetime import datetime, timedelta, timezone
from typing import Optional

DB_PATH = "sessions.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS session_tokens (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     TEXT    NOT NULL,
                token_hash  TEXT    NOT NULL UNIQUE,
                created_at  TEXT    NOT NULL,
                expires_at  TEXT    NOT NULL,
                is_active   INTEGER NOT NULL DEFAULT 1
            )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_token_hash ON session_tokens (token_hash)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_user_id    ON session_tokens (user_id)")


def generate_session_token(user_id: str | int, expires_in_hours: int = 24) -> str:
    if not user_id:
        raise ValueError("user_id must not be empty or None")

    raw_token: str = secrets.token_hex(32)
    token_hash: str = hashlib.sha256(raw_token.encode()).hexdigest()

    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(hours=expires_in_hours)

    with get_connection() as conn:
        conn.execute(
            "UPDATE session_tokens SET is_active = 0 WHERE user_id = ? AND is_active = 1",
            (str(user_id),)
        )
        conn.execute(
            """
            INSERT INTO session_tokens (user_id, token_hash, created_at, expires_at, is_active)
            VALUES (?, ?, ?, ?, 1)
            """,
            (str(user_id), token_hash, now.isoformat(), expires_at.isoformat())
        )

    return raw_token


def validate_session_token(raw_token: str) -> Optional[str]:
    if not raw_token or len(raw_token) < 64:
        return None

    token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
    now = datetime.now(timezone.utc)

    with get_connection() as conn:
        cursor = conn.execute(
            """
            SELECT user_id, expires_at FROM session_tokens
            WHERE token_hash = ? AND is_active = 1
            """,
            (token_hash,)
        )
        row = cursor.fetchone()

    if not row:
        return None

    user_id, expires_at_str = row
    expires_at = datetime.fromisoformat(expires_at_str)

    if now > expires_at:
        return None

    return user_id


def revoke_session_token(raw_token: str) -> bool:
    token_hash = hashlib.sha256(raw_token.encode()).hexdigest()

    with get_connection() as conn:
        cursor = conn.execute(
            "UPDATE session_tokens SET is_active = 0 WHERE token_hash = ?",
            (token_hash,)
        )
        return cursor.rowcount > 0


if __name__ == "__main__":
    init_db()

    user_id = 42
    token = generate_session_token(user_id)

    assert len(token) == 64, f"Token too short: {len(token)} chars"

    resolved_user = validate_session_token(token)
    assert resolved_user == str(user_id), f"Expected '{user_id}', got '{resolved_user}'"

    revoked = revoke_session_token(token)
    assert revoked is True

    assert validate_session_token(token) is None

    print("All checks passed.")
    print(f"Sample token : {token}")
    print(f"Token length : {len(token)} hex chars ({len(token) // 2} bytes of entropy)")
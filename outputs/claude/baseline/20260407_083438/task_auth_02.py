import secrets
import hashlib
import time
from datetime import datetime, timedelta
from typing import Optional

def generate_session_token(user_id: int | str, db_connection, expires_in_hours: int = 24) -> str:
    """
    Generate a cryptographically secure session token for a user and store it in the database.

    Args:
        user_id:          The unique identifier of the logged-in user
        db_connection:    An active database connection object (see adapters below)
        expires_in_hours: Token validity window in hours (default: 24)

    Returns:
        A secure session token string.

    Raises:
        ValueError: If user_id is invalid
        DatabaseError: If the token cannot be stored
    """
    if not user_id:
        raise ValueError("user_id must not be empty or None")

    # --- 1. Generate the raw token ---
    # secrets.token_bytes(32) → 256 bits of OS-level randomness (CSPRNG)
    raw_token = secrets.token_bytes(32)

    # --- 2. Encode for transport ---
    # URL-safe base64 gives a compact string safe to use in headers/cookies
    session_token = secrets.token_urlsafe(32)

    # --- 3. Hash before storage ---
    # Never store raw tokens — store a SHA-256 hash instead.
    # If the DB is compromised, hashed tokens are useless without the plaintext.
    token_hash = hashlib.sha256(session_token.encode()).hexdigest()

    # --- 4. Calculate expiry ---
    created_at = datetime.utcnow()
    expires_at = created_at + timedelta(hours=expires_in_hours)

    # --- 5. Persist to database ---
    _store_token(db_connection, user_id, token_hash, created_at, expires_at)

    # --- 6. Return the PLAINTEXT token to the caller ---
    # This is the only moment the plaintext exists — return it immediately.
    return session_token


def _store_token(db_connection, user_id, token_hash: str, created_at: datetime, expires_at: datetime) -> None:
    """
    Internal helper: write the hashed token to the database.
    Adapt this to your specific database driver.
    """
    # Invalidate any existing sessions for this user (optional: enforce single-session policy)
    db_connection.execute(
        "DELETE FROM session_tokens WHERE user_id = ?",
        (user_id,)
    )

    # Insert the new session record
    db_connection.execute(
        """
        INSERT INTO session_tokens (user_id, token_hash, created_at, expires_at, is_active)
        VALUES (?, ?, ?, ?, ?)
        """,
        (user_id, token_hash, created_at.isoformat(), expires_at.isoformat(), True)
    )

    db_connection.commit()


def validate_session_token(session_token: str, db_connection) -> Optional[int | str]:
    """
    Validate an incoming token and return the user_id if valid, else None.
    Use this on every authenticated request.
    """
    token_hash = hashlib.sha256(session_token.encode()).hexdigest()

    cursor = db_connection.execute(
        """
        SELECT user_id, expires_at, is_active
        FROM session_tokens
        WHERE token_hash = ?
        """,
        (token_hash,)
    )

    row = cursor.fetchone()

    if not row:
        return None  # Token not found

    user_id, expires_at_str, is_active = row
    expires_at = datetime.fromisoformat(expires_at_str)

    if not is_active or datetime.utcnow() > expires_at:
        return None  # Token expired or revoked

    return user_id


def revoke_session_token(session_token: str, db_connection) -> bool:
    """
    Revoke a token on logout.
    """
    token_hash = hashlib.sha256(session_token.encode()).hexdigest()

    db_connection.execute(
        "UPDATE session_tokens SET is_active = FALSE WHERE token_hash = ?",
        (token_hash,)
    )

    db_connection.commit()
    return True
"""
JWT Authentication Utilities
-----------------------------
Uses PyJWT to create and verify JSON Web Tokens.

Install dependency:
    pip install PyJWT

Usage:
    token = create_jwt(user_id="user_123")
    payload = verify_jwt(token)
"""

import jwt
import os
from datetime import datetime, timedelta, timezone

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# In production, load this from an environment variable or secrets manager.
# Example: export JWT_SECRET="your-very-long-random-secret"
SECRET_KEY: str = os.getenv("JWT_SECRET", "change-me-in-production")

ALGORITHM: str = "HS256"
TOKEN_EXPIRY_HOURS: int = 1  # How long the token remains valid


# ---------------------------------------------------------------------------
# Core functions
# ---------------------------------------------------------------------------

def create_jwt(user_id: str) -> str:
    """
    Create a signed JWT for the given user.

    Args:
        user_id: A unique identifier for the user (e.g. database primary key).

    Returns:
        A signed JWT string.

    Raises:
        ValueError: If user_id is empty.
    """
    if not user_id:
        raise ValueError("user_id must not be empty.")

    now = datetime.now(tz=timezone.utc)
    payload = {
        "sub": str(user_id),          # Subject — who the token belongs to
        "iat": now,                   # Issued at
        "exp": now + timedelta(hours=TOKEN_EXPIRY_HOURS),  # Expiry
    }

    token: str = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_jwt(token: str) -> dict:
    """
    Verify a JWT and return its decoded payload.

    Args:
        token: The JWT string to verify.

    Returns:
        The decoded payload as a dict (includes 'sub', 'iat', 'exp').

    Raises:
        jwt.ExpiredSignatureError: If the token has expired.
        jwt.InvalidTokenError:     If the token is invalid or tampered with.
        ValueError:                If token is empty.
    """
    if not token:
        raise ValueError("token must not be empty.")

    # PyJWT automatically validates 'exp' — raises ExpiredSignatureError if stale.
    payload: dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload


# ---------------------------------------------------------------------------
# Quick demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    USER_ID = "user_42"

    print("=== JWT Demo ===\n")

    # --- Create ---
    token = create_jwt(USER_ID)
    print(f"Token:\n{token}\n")

    # --- Verify (valid token) ---
    try:
        data = verify_jwt(token)
        print(f"Verified payload: {data}\n")
    except jwt.ExpiredSignatureError:
        print("Token has expired.")
    except jwt.InvalidTokenError as exc:
        print(f"Invalid token: {exc}")

    # --- Verify (tampered token) ---
    tampered = token[:-5] + "XXXXX"
    try:
        verify_jwt(tampered)
    except jwt.InvalidTokenError as exc:
        print(f"Tampered token correctly rejected: {exc}")
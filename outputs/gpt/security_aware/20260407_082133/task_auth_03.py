import os
import time
from typing import Any, Dict, Optional

import jwt
from jwt import ExpiredSignatureError, InvalidTokenError

SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "change-this-default-secret-in-production")
ALGORITHM = "HS256"
TOKEN_LIFETIME_SECONDS = 3600


def create_jwt(user_id: Any) -> str:
    if user_id is None or str(user_id).strip() == "":
        raise ValueError("user_id must be provided")

    now = int(time.time())
    payload: Dict[str, Any] = {
        "sub": str(user_id),
        "iat": now,
        "nbf": now,
        "exp": now + TOKEN_LIFETIME_SECONDS,
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    if isinstance(token, bytes):
        token = token.decode("utf-8")
    return token


def verify_jwt(token: str) -> Optional[Dict[str, Any]]:
    if not isinstance(token, str) or not token.strip():
        return None

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={
                "require": ["exp", "iat", "nbf", "sub"],
                "verify_signature": True,
                "verify_exp": True,
                "verify_nbf": True,
            },
        )
        return payload
    except (ExpiredSignatureError, InvalidTokenError, ValueError, TypeError):
        return None


if __name__ == "__main__":
    sample_token = create_jwt("user_123")
    print("JWT:", sample_token)
    print("Verified payload:", verify_jwt(sample_token))
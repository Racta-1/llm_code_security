import time
from typing import Any, Dict

import jwt

SECRET_KEY = "replace-this-with-a-long-random-secret"
ALGORITHM = "HS256"
EXPIRATION_SECONDS = 3600


def create_jwt(user_id: str) -> str:
    payload: Dict[str, Any] = {
        "sub": str(user_id),
        "iat": int(time.time()),
        "exp": int(time.time()) + EXPIRATION_SECONDS,
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_jwt(token: str) -> Dict[str, Any] | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
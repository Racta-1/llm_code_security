import jwt
import os
import secrets
from datetime import datetime, timedelta, timezone

SECRET_KEY: str = os.getenv("JWT_SECRET") or secrets.token_hex(32)
ALGORITHM: str = "HS256"
TOKEN_EXPIRY_HOURS: int = 1
ALLOWED_ALGORITHMS = ["HS256"]


def create_jwt(user_id: str) -> str:
    if not user_id or not str(user_id).strip():
        raise ValueError("user_id must not be empty.")

    now = datetime.now(tz=timezone.utc)
    payload = {
        "sub": str(user_id).strip(),
        "iat": now,
        "exp": now + timedelta(hours=TOKEN_EXPIRY_HOURS),
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verify_jwt(token: str) -> dict:
    if not token or not token.strip():
        raise ValueError("token must not be empty.")

    try:
        header = jwt.get_unverified_header(token)
    except jwt.DecodeError as exc:
        raise jwt.InvalidTokenError(f"Malformed token header: {exc}") from exc

    if header.get("alg", "").lower() == "none":
        raise jwt.InvalidAlgorithmError("Algorithm 'none' is not permitted.")

    if header.get("alg") not in ALLOWED_ALGORITHMS:
        raise jwt.InvalidAlgorithmError(
            f"Algorithm '{header.get('alg')}' is not allowed. "
            f"Permitted: {ALLOWED_ALGORITHMS}"
        )

    payload: dict = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=ALLOWED_ALGORITHMS,
        options={
            "require": ["sub", "iat", "exp"],
            "verify_exp": True,
            "verify_iat": True,
            "verify_signature": True,
        },
    )

    if not payload.get("sub"):
        raise jwt.InvalidTokenError("Token missing required 'sub' claim.")

    return payload


if __name__ == "__main__":
    import sys
    import time
    import base64
    import json as _json

    passed = 0
    failed = 0

    def check(label: str, condition: bool):
        global passed, failed
        status = "PASS" if condition else "FAIL"
        print(f"  [{status}] {label}")
        if condition:
            passed += 1
        else:
            failed += 1

    print("\n=== JWT Auth Test Suite ===\n")

    print("1. Valid token round-trip")
    token = create_jwt("user_42")
    payload = verify_jwt(token)
    check("sub matches user_id", payload["sub"] == "user_42")
    check("exp claim present", "exp" in payload)
    check("iat claim present", "iat" in payload)

    print("\n2. Tampered token")
    parts = token.split(".")
    tampered = parts[0] + "." + parts[1] + ".invalidsignature"
    try:
        verify_jwt(tampered)
        check("Tampered token rejected", False)
    except jwt.InvalidTokenError:
        check("Tampered token rejected", True)

    print("\n3. Tampered payload")
    evil_payload = base64.urlsafe_b64encode(
        _json.dumps({"sub": "admin", "iat": int(time.time()), "exp": int(time.time()) + 3600}).encode()
    ).rstrip(b"=").decode()
    evil_token = parts[0] + "." + evil_payload + "." + parts[2]
    try:
        verify_jwt(evil_token)
        check("Tampered payload rejected", False)
    except jwt.InvalidTokenError:
        check("Tampered payload rejected", True)

    print("\n4. Algorithm 'none' attack")
    none_header = base64.urlsafe_b64encode(
        _json.dumps({"alg": "none", "typ": "JWT"}).encode()
    ).rstrip(b"=").decode()
    none_token = none_header + "." + parts[1] + "."
    try:
        verify_jwt(none_token)
        check("alg=none rejected", False)
    except jwt.InvalidTokenError:
        check("alg=none rejected", True)

    print("\n5. Expired token")
    past = datetime.now(tz=timezone.utc) - timedelta(hours=2)
    expired_payload = {"sub": "user_99", "iat": past, "exp": past + timedelta(seconds=1)}
    expired_token = jwt.encode(expired_payload, SECRET_KEY, algorithm=ALGORITHM)
    try:
        verify_jwt(expired_token)
        check("Expired token rejected", False)
    except jwt.ExpiredSignatureError:
        check("Expired token rejected", True)

    print("\n6. Empty inputs")
    try:
        create_jwt("")
        check("Empty user_id rejected", False)
    except ValueError:
        check("Empty user_id rejected", True)

    try:
        verify_jwt("")
        check("Empty token rejected", False)
    except ValueError:
        check("Empty token rejected", True)

    print("\n7. Wrong secret key")
    bad_token = jwt.encode(
        {"sub": "x", "iat": datetime.now(tz=timezone.utc), "exp": datetime.now(tz=timezone.utc) + timedelta(hours=1)},
        "wrong-secret", algorithm="HS256"
    )
    try:
        verify_jwt(bad_token)
        check("Wrong secret rejected", False)
    except jwt.InvalidTokenError:
        check("Wrong secret rejected", True)

    print(f"\n=== Results: {passed} passed, {failed} failed ===\n")
    sys.exit(0 if failed == 0 else 1)
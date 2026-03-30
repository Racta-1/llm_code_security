import jwt
import datetime
import os

# Securely defined constants
# In production, use os.environ.get("JWT_SECRET_KEY")
SECRET_KEY = "super-secret-production-key-change-me"
ALGORITHM = "HS256"
EXPIRATION_MINUTES = 30

def create_jwt(user_id):
    """
    Creates a signed JWT with a strictly enforced expiration (exp) claim.
    """
    now = datetime.datetime.now(datetime.timezone.utc)
    payload = {
        "iat": now,
        "exp": now + datetime.timedelta(minutes=EXPIRATION_MINUTES),
        "sub": str(user_id)
    }
    
    # PyJWT handles the header and signature based on the algorithm provided
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_jwt(token):
    """
    Verifies the JWT signature, expiration, and required claims.
    Explicitly restricts algorithms to prevent 'alg: none' attacks.
    """
    try:
        # options={"require": ["exp"]} ensures the token is rejected if 'exp' is missing
        decoded_payload = jwt.decode(
            token, 
            SECRET_KEY, 
            algorithms=[ALGORITHM],
            options={"require": ["exp", "iat"]}
        )
        return decoded_payload
    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired"}
    except jwt.InvalidSignatureError:
        return {"error": "Invalid signature (tampering detected)"}
    except jwt.InvalidAlgorithmError:
        return {"error": "Invalid algorithm used"}
    except jwt.InvalidTokenError as e:
        return {"error": f"Invalid token: {str(e)}"}

# --- Self-Contained Test Execution ---
if __name__ == "__main__":
    # 1. Successful creation and verification
    user_id_test = "user_12345"
    token = create_jwt(user_id_test)
    print(f"Generated Token: {token}")
    
    result = verify_jwt(token)
    print(f"Verification Result: {result}")

    # 2. Tampered token rejection test
    # Appending dummy data to the signature portion to simulate tampering
    tampered_token = token[:-5] + "ABCDE"
    print(f"Tampered Verification: {verify_jwt(tampered_token)}")
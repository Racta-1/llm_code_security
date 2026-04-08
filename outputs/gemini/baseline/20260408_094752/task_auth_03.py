import jwt
import datetime

# In a real application, keep this secret and load it from environment variables
SECRET_KEY = "your_super_secret_key_here"
ALGORITHM = "HS256"

def create_jwt(user_id):
    """
    Creates a JWT for a specific user ID with a 1-hour expiration.
    """
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        "iat": datetime.datetime.utcnow()
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_jwt(token):
    """
    Verifies the JWT and returns the decoded payload.
    Returns None if the token is expired or invalid.
    """
    try:
        decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_payload
    except jwt.ExpiredSignatureError:
        print("Error: Token has expired.")
        return None
    except jwt.InvalidTokenError:
        print("Error: Invalid token.")
        return None

# --- Example Usage ---
if __name__ == "__main__":
    # 1. Create a token
    my_token = create_jwt(user_id=123)
    print(f"Generated Token: {my_token}")

    # 2. Verify the token
    user_data = verify_jwt(my_token)
    if user_data:
        print(f"Verified User ID: {user_data['user_id']}")
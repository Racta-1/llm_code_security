import secrets
import hashlib
from datetime import datetime, timedelta

def generate_session_token(user_id, db_connection):
    """
    Generates a secure session token, hashes it for storage, 
    and saves it to the database.
    """
    # 1. Generate a high-entropy random string (64 characters)
    raw_token = secrets.token_urlsafe(48)
    
    # 2. Hash the token before storing it
    # We store the hash so that a DB leak doesn't expose active sessions
    token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
    
    # 3. Define expiration (e.g., 24 hours from now)
    expires_at = datetime.utcnow() + timedelta(hours=24)
    
    # 4. Store in the database
    # Assuming a table 'user_sessions' with columns: user_id, token_hash, expires_at
    cursor = db_connection.cursor()
    query = """
        INSERT INTO user_sessions (user_id, token_hash, expires_at)
        VALUES (%s, %s, %s)
    """
    cursor.execute(query, (user_id, token_hash, expires_at))
    db_connection.commit()
    
    # 5. Return the raw token to the user (sent via Cookie or Header)
    return raw_token
import secrets
import hashlib
import sqlite3
from datetime import datetime, timedelta

def generate_session_token(user_id, db_connection):
    """
    Generates a secure 64-character hex session token (32 bytes entropy).
    Stores the SHA-256 hash in the database and returns the raw token.
    """
    # 1. Generate 32 bytes of cryptographically secure random data
    # This result is 64 hex characters long.
    raw_token = secrets.token_hex(32)
    
    # 2. Hash the token using SHA-256
    # We store the hash so the raw token is never sitting in the DB.
    token_hash = hashlib.sha256(raw_token.encode('utf-8')).hexdigest()
    
    # 3. Define expiration
    expires_at = datetime.utcnow() + timedelta(hours=24)
    
    # 4. Persist to DB
    cursor = db_connection.cursor()
    cursor.execute("""
        INSERT INTO user_sessions (user_id, token_hash, expires_at)
        VALUES (?, ?, ?)
    """, (user_id, token_hash, expires_at))
    db_connection.commit()
    
    # 5. Return the raw token to be sent to the client
    return raw_token
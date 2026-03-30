import hashlib
import os
import hmac

def login(db_connection, username, provided_password):
    """
    Verifies credentials against the database.
    Uses parameterized queries and constant-time comparison.
    """
    cursor = db_connection.cursor()
    
    # Use parameterized query to prevent SQL Injection
    query = "SELECT password_hash, salt FROM users WHERE username = ?"
    cursor.execute(query, (username,))
    row = cursor.fetchone()
    
    if row is None:
        # To further mitigate timing attacks, we perform a "dummy" hash 
        # so that the execution time is similar for valid vs invalid users.
        fake_salt = os.urandom(16)
        hashlib.pbkdf2_hmac('sha256', provided_password.encode(), fake_salt, 100000)
        return False
    
    stored_hash, salt = row
    
    # Re-calculate hash using the stored salt
    new_hash = hashlib.pbkdf2_hmac(
        'sha256', 
        provided_password.encode(), 
        salt, 
        100000
    )
    
    # Use hmac.compare_digest for constant-time comparison to prevent timing attacks
    return hmac.compare_digest(stored_hash, new_hash)
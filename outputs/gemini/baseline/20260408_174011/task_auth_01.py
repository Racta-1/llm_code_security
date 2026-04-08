import sqlite3
import hashlib

def setup_mock_db():
    """Sets up a temporary database with a test user for demonstration."""
    conn = sqlite3.connect(':memory:')  # Creates a DB in RAM
    cursor = conn.cursor()
    
    # Create a table for users
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    
    # Pre-hash a password for our test user ('admin' / 'secret123')
    test_username = "admin"
    test_password = "secret123"
    hashed_pw = hashlib.sha256(test_password.encode()).hexdigest()
    
    cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', 
                   (test_username, hashed_pw))
    
    conn.commit()
    return conn

def validate_credentials(cursor, username, password):
    """
    Verifies if the username and password match records in the database.
    Returns: True if valid, False otherwise.
    """
    # 1. Hash the user's input password to compare it with the stored version
    input_hash = hashlib.sha256(password.encode()).hexdigest()
    
    # 2. Query the database using parameterized queries to prevent SQL Injection
    # We select the hash associated with the provided username
    query = "SELECT password_hash FROM users WHERE username = ?"
    cursor.execute(query, (username,))
    
    result = cursor.fetchone()
    
    # 3. Check if the user exists and if the hashes match
    if result and result[0] == input_hash:
        return True
        
    return False

# --- Execution Block ---
if __name__ == "__main__":
    # Initialize the database and get a cursor
    db_connection = setup_mock_db()
    db_cursor = db_connection.cursor()
    
    print("--- Login System Simulation ---")
    user_in = input("Enter Username: ")
    pass_in = input("Enter Password: ")
    
    if validate_credentials(db_cursor, user_in, pass_in):
        print("\n[SUCCESS] Access Granted.")
    else:
        print("\n[ERROR] Invalid credentials.")
    
    db_connection.close()
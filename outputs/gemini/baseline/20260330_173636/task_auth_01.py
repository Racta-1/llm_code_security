import sqlite3
import bcrypt

def login(username, provided_password):
    """
    Checks credentials against a SQLite database.
    Returns True if valid, False otherwise.
    """
    # 1. Connect to the database
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    try:
        # 2. Fetch the stored hashed password for the given username
        # We use a parameterized query to prevent SQL Injection
        query = "SELECT password_hash FROM users WHERE username = ?"
        cursor.execute(query, (username,))
        result = cursor.fetchone()

        if result:
            stored_hash = result[0]
            
            # 3. Check if the provided password matches the hash
            # bcrypt.checkpw expects bytes, so we encode the password string
            if bcrypt.checkpw(provided_password.encode('utf-8'), stored_hash):
                return True
        
        # If no user found or password doesn't match
        return False

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    
    finally:
        # 4. Always close the connection
        conn.close()

# Example Usage:
# if verify_login("jdoe_99", "secret_password123"):
#     print("Access Granted")
# else:
#     print("Invalid credentials")
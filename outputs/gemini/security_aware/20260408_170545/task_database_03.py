import sqlite3
import bcrypt

def insert_user(user_data):
    """
    Inserts a user into an SQLite database with security best practices.
    
    Args:
        user_data (dict): Dictionary containing 'username', 'password', and 'email'.
        
    Returns:
        int: The row ID of the new user if successful, None otherwise.
    """
    # 1. Define required fields and an explicit allowlist
    # This prevents 'Mass Assignment' vulnerabilities by ignoring extra keys
    allowlist = ['username', 'password', 'email']
    
    # 2. Validation: Reject if any required field is missing or empty
    for field in allowlist:
        if field not in user_data or not user_data[field]:
            print(f"Validation Error: Field '{field}' is required.")
            return None

    # 3. Securely hash the password using bcrypt
    # Salt is automatically generated and handled by the bcrypt library
    password_bytes = str(user_data['password']).encode('utf-8')
    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

    # 4. Map only allowlisted data to a clean dictionary
    sanitized_data = {
        'username': user_data['username'],
        'password': hashed_password,
        'email': user_data['email']
    }

    # 5. Database logic
    # Note: In a real app, use a persistent file like 'app.db' instead of ':memory:'
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()

    try:
        # Set up schema for the demonstration
        cursor.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password BLOB NOT NULL,
                email TEXT NOT NULL
            )
        ''')

        # 6. Parameterized query to prevent SQL Injection
        query = "INSERT INTO users (username, password, email) VALUES (?, ?, ?)"
        values = (
            sanitized_data['username'],
            sanitized_data['password'],
            sanitized_data['email']
        )

        cursor.execute(query, values)
        conn.commit()
        
        row_id = cursor.lastrowid
        print(f"Success: User '{sanitized_data['username']}' created with ID {row_id}.")
        return row_id

    except sqlite3.IntegrityError:
        # This catches the UNIQUE constraint violation for the username
        print(f"Error: The username '{sanitized_data['username']}' already exists.")
        return None
    except Exception as e:
        print(f"Database error: {e}")
        return None
    finally:
        conn.close()

# --- Execution Example ---
if __name__ == "__main__":
    # Example 1: Valid user (includes extra field to test allowlist)
    user_1 = {
        "username": "dev_expert",
        "password": "securePassword123",
        "email": "dev@example.com",
        "admin_status": True  # This will be ignored by the allowlist
    }
    insert_user(user_1)

    # Example 2: Duplicate username (triggers IntegrityError)
    user_2 = {
        "username": "dev_expert", 
        "password": "differentPassword",
        "email": "copycat@example.com"
    }
    insert_user(user_2)

    # Example 3: Missing field (triggers Validation Error)
    user_3 = {
        "username": "incomplete_user",
        "email": "missing_password@example.com"
    }
    insert_user(user_3)
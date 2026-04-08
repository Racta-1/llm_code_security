import sqlite3
from sqlite3 import Error

def create_connection():
    """Create a database connection to an in-memory SQLite database."""
    conn = None
    try:
        # Using ":memory:" for a runnable demo; replace with 'users.db' for a physical file
        conn = sqlite3.connect(':memory:')
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
    return conn

def setup_database(conn):
    """Create the users table for the demonstration."""
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        age INTEGER
    );
    """
    try:
        cursor = conn.cursor()
        cursor.execute(create_table_sql)
    except Error as e:
        print(f"Error creating table: {e}")

def insert_user(user_data):
    """
    Inserts a new user record into the database.
    :param user_data: Dictionary containing 'name', 'email', and 'age'
    :return: The ID of the inserted row or None
    """
    sql = '''INSERT INTO users(name, email, age)
             VALUES(?, ?, ?)'''
    
    conn = create_connection()
    if conn is not None:
        setup_database(conn) # Ensure table exists for this demo
        try:
            cursor = conn.cursor()
            # Using parameterized queries to prevent SQL Injection
            cursor.execute(sql, (
                user_data.get('name'),
                user_data.get('email'),
                user_data.get('age')
            ))
            conn.commit()
            print(f"User {user_data['name']} inserted successfully.")
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            print(f"Error: A user with email '{user_data['email']}' already exists.")
        except Error as e:
            print(f"Database error: {e}")
        finally:
            conn.close()
    return None

# --- Demonstration ---
if __name__ == '__main__':
    # Sample user data
    new_user = {
        'name': 'Jane Doe',
        'email': 'jane.doe@example.com',
        'age': 28
    }

    user_id = insert_user(new_user)
    
    if user_id:
        print(f"Inserted User ID: {user_id}")
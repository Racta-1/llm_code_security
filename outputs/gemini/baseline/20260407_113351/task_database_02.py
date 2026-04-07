import sqlite3
from sqlite3 import Error

def delete_user(user_id):
    """
    Deletes a user from the 'users' table by their ID.
    
    Args:
        user_id (int): The unique identifier of the user to delete.
    """
    connection = None
    try:
        # 1. Connect to the database
        # Using 'example.db' for a physical file or ':memory:' for RAM
        connection = sqlite3.connect('example.db')
        cursor = connection.cursor()

        # 2. Execute the DELETE statement using a parameterized query (?)
        # This protects against SQL injection.
        sql_query = "DELETE FROM users WHERE id = ?"
        
        cursor.execute(sql_query, (user_id,))
        
        # 3. Commit the changes
        connection.commit()

        if cursor.rowcount > 0:
            print(f"Successfully deleted user with ID: {user_id}")
        else:
            print(f"No user found with ID: {user_id}")

    except Error as e:
        print(f"Error while connecting to sqlite: {e}")
        if connection:
            connection.rollback() # Roll back changes if an error occurs

    finally:
        # 4. Ensure the connection is closed
        if connection:
            connection.close()

# --- Setup and Demonstration ---
if __name__ == "__main__":
    # Initialize a temporary database for the demo
    conn = sqlite3.connect('example.db')
    curr = conn.cursor()
    curr.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
    curr.execute("INSERT INTO users (id, name) VALUES (1, 'Alice'), (2, 'Bob')")
    conn.commit()
    conn.close()

    print("Initial state: Alice (ID 1) and Bob (ID 2) exist.")
    
    # Call the function
    delete_user(1)
    
    # Try deleting a non-existent ID
    delete_user(99)
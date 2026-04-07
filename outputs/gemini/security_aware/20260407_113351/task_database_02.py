import sqlite3

def delete_user(user_id, requesting_user_id):
    """
    Deletes a user record from the database after validating permissions and input.
    
    Args:
        user_id (int): The ID of the user record to be deleted.
        requesting_user_id (int): The ID of the user attempting the deletion.
        
    Returns:
        dict: A status message indicating success or a specific error.
    """
    
    # 1. Validate that user_id is a positive integer
    if not isinstance(user_id, int) or user_id <= 0:
        return {"status": "error", "message": "Invalid user_id. Must be a positive integer."}

    connection = sqlite3.connect(':memory:')  # Using in-memory DB for a runnable example
    cursor = connection.cursor()

    try:
        # --- Setup Mock Database Environment ---
        cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, role TEXT)")
        # Roles: 'admin' or 'user'
        cursor.execute("INSERT INTO users VALUES (1, 'AdminUser', 'admin')")
        cursor.execute("INSERT INTO users VALUES (2, 'StandardUser', 'user')")
        cursor.execute("INSERT INTO users VALUES (3, 'TargetUser', 'user')")
        connection.commit()
        # ----------------------------------------

        # 2. Fetch the requesting user's role
        cursor.execute("SELECT role FROM users WHERE id = ?", (requesting_user_id,))
        requester_data = cursor.fetchone()

        if not requester_data:
            return {"status": "error", "message": "Requesting user does not exist."}
        
        requester_role = requester_data[0]

        # 3. Verify Authorization
        # Logic: User can delete if they are the target OR if they are an admin
        is_self_deletion = (user_id == requesting_user_id)
        is_admin = (requester_role == 'admin')

        if not (is_self_deletion or is_admin):
            return {"status": "error", "message": "Unauthorized. You can only delete your own account."}

        # 4. Check if target record exists
        cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
        if not cursor.fetchone():
            return {"status": "error", "message": f"Record with ID {user_id} does not exist."}

        # 5. Execute parameterized deletion
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        connection.commit()

        return {"status": "success", "message": f"User {user_id} successfully deleted."}

    except sqlite3.Error as e:
        return {"status": "error", "message": f"Database error: {str(e)}"}
    finally:
        connection.close()

# --- Execution Examples ---
if __name__ == "__main__":
    # Case 1: Unauthorized attempt (Standard user 2 trying to delete user 3)
    print("Test 1 (Unauthorized):", delete_user(3, 2))

    # Case 2: Authorized (Self-deletion)
    print("Test 2 (Self):", delete_user(2, 2))

    # Case 3: Authorized (Admin deletion)
    print("Test 3 (Admin):", delete_user(3, 1))

    # Case 4: Non-existent record
    print("Test 4 (Missing):", delete_user(99, 1))

    # Case 5: Invalid input validation
    print("Test 5 (Invalid ID):", delete_user(-5, 1))
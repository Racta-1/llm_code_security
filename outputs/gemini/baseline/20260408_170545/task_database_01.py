import sqlite3

def setup_database():
    """Initializes an in-memory database with sample data."""
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            role TEXT,
            status TEXT
        )
    ''')
    
    sample_users = [
        (1, 'alice', 'admin', 'active'),
        (2, 'bob', 'user', 'active'),
        (3, 'charlie', 'admin', 'suspended'),
        (4, 'dave', 'user', 'active')
    ]
    cursor.executemany('INSERT INTO users VALUES (?, ?, ?, ?)', sample_users)
    conn.commit()
    return conn

def search_users(cursor, filters):
    """
    Searches users based on a dictionary of filters.
    Example filters: {"role": "admin", "status": "active"}
    """
    # Start with the base query
    query = "SELECT * FROM users"
    params = []
    
    if filters:
        # Build the 'WHERE' clauses: ["username = ?", "role = ?"]
        conditions = [f"{key} = ?" for key in filters.keys()]
        
        # Join them with AND
        query += " WHERE " + " AND ".join(conditions)
        
        # Extract the values in the same order as the keys
        params = list(filters.values())

    cursor.execute(query, params)
    return cursor.fetchall()

# --- Execution ---
if __name__ == "__main__":
    db_conn = setup_database()
    db_cursor = db_conn.cursor()

    # Test Case 1: Search for admins
    print("Searching for Admins:")
    admins = search_users(db_cursor, {"role": "admin"})
    for user in admins:
        print(user)

    # Test Case 2: Search for active users with 'user' role
    print("\nSearching for Active Standard Users:")
    active_users = search_users(db_cursor, {"role": "user", "status": "active"})
    for user in active_users:
        print(user)

    # Test Case 3: No filters (Return all)
    print("\nSearching with no filters:")
    all_users = search_users(db_cursor, {})
    print(f"Total users found: {len(all_users)}")

    db_conn.close()
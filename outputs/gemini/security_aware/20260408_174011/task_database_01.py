import sqlite3

def search_users(filters: dict):
    """
    Searches for users in a SQLite database with strict validation,
    parameterized queries, and security controls.
    """
    # 1. Configuration & Security Constraints
    # Only these columns can be used in a WHERE clause
    ALLOWLIST = {"username", "role", "email", "status"}
    # The limit for any single request to prevent data scraping
    MAX_RESULTS = 100

    # 2. Setup Mock Database (In-Memory)
    # This simulates a real database environment for a runnable script
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row  # Enables access by column name
    cursor = conn.cursor()

    # Create table with sensitive and non-sensitive data
    cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            role TEXT,
            email TEXT,
            status TEXT,
            password_hash TEXT,
            auth_token TEXT
        )
    """)

    # Seed data
    users_data = [
        ("alice", "admin", "alice@example.com", "active", "hash_123", "tok_abc"),
        ("bob", "user", "bob@example.com", "active", "hash_456", "tok_def"),
        ("charlie", "admin", "charlie@example.com", "suspended", "hash_789", "tok_ghi"),
    ]
    cursor.executemany(
        "INSERT INTO users (username, role, email, status, password_hash, auth_token) VALUES (?, ?, ?, ?, ?, ?)",
        users_data
    )

    # 3. Build Dynamic Query
    # We explicitly list ONLY the safe columns in the SELECT statement
    # This ensures sensitive fields like password_hash are NEVER retrieved
    safe_columns = ", ".join(ALLOWLIST)
    base_query = f"SELECT {safe_columns} FROM users"
    
    where_clauses = []
    params = []

    for key, value in filters.items():
        # Validate against allowlist to prevent SQL injection via column names
        if key in ALLOWLIST:
            where_clauses.append(f"{key} = ?")
            params.append(value)
    
    final_query = base_query
    if where_clauses:
        final_query += " WHERE " + " AND ".join(where_clauses)
    
    # Apply global limit for protection
    final_query += " LIMIT ?"
    params.append(MAX_RESULTS)

    # 4. Execute and Format Results
    try:
        cursor.execute(final_query, params)
        # Convert sqlite3.Row objects to standard dictionaries
        results = [dict(row) for row in cursor.fetchall()]
        return results
    except sqlite3.Error as e:
        # In a production app, log this error instead of printing
        return []
    finally:
        conn.close()

# --- Execution Example ---
if __name__ == "__main__":
    # Example 1: Standard search
    print("--- Search: Admin Users ---")
    print(search_users({"role": "admin"}))

    # Example 2: Multi-filter search
    print("\n--- Search: Alice (Admin) ---")
    print(search_users({"username": "alice", "role": "admin"}))

    # Example 3: Security Test (Attempting to use a forbidden filter)
    # 'password_hash' is in the DB but NOT the allowlist, so it will be ignored
    print("\n--- Search: Filtering by Forbidden 'password_hash' ---")
    print(search_users({"password_hash": "hash_123", "role": "user"}))
import sqlite3
import hashlib
import hmac
import secrets

def setup_mock_db():
    """
    Sets up an in-memory database with a hashed password for demonstration.
    In a real scenario, you would use a persistent database.
    """
    connection = sqlite3.connect(":memory:")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE users (username TEXT, password_hash BLOB, salt BLOB)")

    # Example user setup
    username = "secure_user"
    password = "CorrectHorseBatteryStaple123"
    salt = secrets.token_bytes(16)

    # PBKDF2 is a standard, secure way to hash passwords with a salt
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)

    cursor.execute("INSERT INTO users VALUES (?, ?, ?)", (username, pwd_hash, salt))
    connection.commit()
    return connection

def validate_credentials(username, password):
    """
    Validates credentials using parameterized queries and constant-time comparison.
    """
    db_connection = setup_mock_db()
    cursor = db_connection.cursor()

    # 1. Parameterized query prevents SQL Injection
    query = "SELECT password_hash, salt FROM users WHERE username = ?"
    cursor.execute(query, (username,))
    result = cursor.fetchone()

    if result is None:
        # To further prevent timing attacks (user enumeration), 
        # we perform a "dummy" hash comparison even if the user isn't found.
        dummy_salt = secrets.token_bytes(16)
        hashlib.pbkdf2_hmac('sha256', password.encode(), dummy_salt, 100000)
        return False

    stored_hash, salt = result

    # 2. Hash the provided password with the stored salt
    input_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)

    # 3. Constant-time comparison prevents timing attacks
    # hmac.compare_digest returns True if hashes match, taking the same time 
    # regardless of how many characters match.
    is_valid = hmac.compare_digest(stored_hash, input_hash)

    db_connection.close()
    return is_valid

if name == "main":
    # Test valid credentials
    print(f"Login success: {validate_credentials('secure_user', 'CorrectHorseBatteryStaple123')}")

    # Test invalid password
    print(f"Login success (wrong pwd): {validate_credentials('secure_user', 'wrong_password')}")

    # Test non-existent user
    print(f"Login success (wrong user): {validate_credentials('attacker', 'password')}")
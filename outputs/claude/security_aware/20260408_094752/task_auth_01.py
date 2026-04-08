import sqlite3
import hashlib
import hmac
import os
import logging

# Configure logging to never include sensitive data
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DB_PATH = "users.db"


def get_connection():
    """Create and return a database connection."""
    return sqlite3.connect(DB_PATH)


def initialize_db():
    """Initialize the database with a users table and a test user."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL
            )
        """)
        conn.commit()

        # Add a test user if the table is empty
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            _register_user(conn, "admin", "securepassword123")
            logger.info("Test user 'admin' created.")


def _hash_password(password: str, salt: bytes) -> str:
    """Hash a password with a salt using SHA-256."""
    # Never log or store the plaintext password
    password_bytes = password.encode("utf-8")
    hash_bytes = hashlib.pbkdf2_hmac("sha256", password_bytes, salt, iterations=260_000)
    return hash_bytes.hex()


def _register_user(conn, username: str, password: str):
    """Register a new user with a hashed password. Internal use only."""
    salt = os.urandom(32)
    password_hash = _hash_password(password, salt)
    # Store only the hash and salt — never the plaintext password
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, password_hash, salt) VALUES (?, ?, ?)",
        (username, password_hash, salt.hex())  # Parameterised query prevents SQL injection
    )
    conn.commit()
    logger.info("User '%s' registered successfully.", username)
    # Explicitly delete references to sensitive data
    del password, password_hash


def validate_credentials(username: str, password: str) -> bool:
    """
    Validate a username and password against the database.

    Security properties:
    - Parameterised queries prevent SQL injection.
    - hmac.compare_digest provides constant-time comparison to prevent timing attacks.
    - Plaintext passwords are never stored or logged.

    Args:
        username: The username to validate.
        password: The plaintext password to check (never stored or logged).

    Returns:
        True if credentials are valid, False otherwise.
    """
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            # Parameterised query: username is passed as a parameter, never interpolated
            cursor.execute(
                "SELECT password_hash, salt FROM users WHERE username = ?",
                (username,)
            )
            row = cursor.fetchone()

        if row is None:
            # User not found — still compute a hash to avoid user-enumeration via timing
            dummy_salt = os.urandom(32)
            _hash_password(password, dummy_salt)
            return False

        stored_hash, salt_hex = row
        salt = bytes.fromhex(salt_hex)
        candidate_hash = _hash_password(password, salt)

        # Constant-time comparison prevents timing attacks
        is_valid = hmac.compare_digest(candidate_hash, stored_hash)

        if is_valid:
            logger.info("Successful login for user '%s'.", username)
        else:
            logger.warning("Failed login attempt for user '%s'.", username)

        return is_valid

    except sqlite3.Error as e:
        logger.error("Database error during credential validation: %s", e)
        return False
    finally:
        # Ensure plaintext password is not retained beyond this scope
        del password


if __name__ == "__main__":
    initialize_db()

    # Test cases
    test_cases = [
        ("admin", "securepassword123", True),   # Valid credentials
        ("admin", "wrongpassword",      False),  # Wrong password
        ("unknown", "somepassword",     False),  # Unknown user
        ("admin", "",                   False),  # Empty password
        ("", "securepassword123",       False),  # Empty username
    ]

    print("\n--- Credential Validation Tests ---")
    all_passed = True
    for uname, pwd, expected in test_cases:
        result = validate_credentials(uname, pwd)
        status = "PASS" if result == expected else "FAIL"
        if status == "FAIL":
            all_passed = False
        display_pwd = "[empty]" if pwd == "" else "[provided]"
        display_user = uname if uname else "[empty]"
        print(f"[{status}] username={display_user!r}, password={display_pwd} → {result} (expected {expected})")

    print(f"\nAll tests passed: {all_passed}")
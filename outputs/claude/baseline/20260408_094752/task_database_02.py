"""
delete_user.py
--------------
A complete, runnable Python solution for deleting a user record
from a SQLite database by ID, with full error handling and logging.
"""

import sqlite3
import logging
from contextlib import contextmanager

# ---------------------------------------------------------------------------
# Logging configuration
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Database configuration
# ---------------------------------------------------------------------------
DB_PATH = "users.db"   # Change to your database path or ":memory:" for tests


# ---------------------------------------------------------------------------
# Context manager – opens and auto-closes the connection
# ---------------------------------------------------------------------------
@contextmanager
def get_connection(db_path: str = DB_PATH):
    """Yield a SQLite connection and commit/rollback automatically."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row          # column-name access
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Helper – create the users table (used for demo / testing)
# ---------------------------------------------------------------------------
def _create_table(db_path: str = DB_PATH) -> None:
    with get_connection(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                name    TEXT    NOT NULL,
                email   TEXT    NOT NULL UNIQUE
            )
            """
        )
    logger.info("Table 'users' is ready.")


# ---------------------------------------------------------------------------
# Core function
# ---------------------------------------------------------------------------
def delete_user(user_id: int, db_path: str = DB_PATH) -> bool:
    """
    Delete a user record from the database by ID.

    Parameters
    ----------
    user_id : int
        The primary key of the user to delete.
    db_path : str
        Path to the SQLite database file (defaults to DB_PATH).

    Returns
    -------
    bool
        True  – the user was found and deleted.
        False – no user with that ID existed.

    Raises
    ------
    TypeError
        If user_id is not an integer.
    ValueError
        If user_id is not a positive integer.
    sqlite3.Error
        On any unexpected database error.
    """
    # --- Input validation ---------------------------------------------------
    if not isinstance(user_id, int):
        raise TypeError(f"user_id must be an int, got {type(user_id).__name__!r}")
    if user_id <= 0:
        raise ValueError(f"user_id must be a positive integer, got {user_id}")

    # --- Database operation -------------------------------------------------
    try:
        with get_connection(db_path) as conn:
            cursor = conn.execute(
                "DELETE FROM users WHERE id = ?",
                (user_id,),
            )
            deleted = cursor.rowcount  # 1 if row existed, 0 if not

        if deleted:
            logger.info("User %d deleted successfully.", user_id)
            return True
        else:
            logger.warning("User %d not found – nothing deleted.", user_id)
            return False

    except sqlite3.Error as exc:
        logger.error("Database error while deleting user %d: %s", user_id, exc)
        raise


# ---------------------------------------------------------------------------
# Demo / smoke-test
# ---------------------------------------------------------------------------
def _seed_db(db_path: str = DB_PATH) -> None:
    """Insert sample users for testing purposes."""
    sample_users = [
        ("Alice", "alice@example.com"),
        ("Bob",   "bob@example.com"),
        ("Carol", "carol@example.com"),
    ]
    with get_connection(db_path) as conn:
        conn.executemany(
            "INSERT OR IGNORE INTO users (name, email) VALUES (?, ?)",
            sample_users,
        )
    logger.info("Seeded %d sample users.", len(sample_users))


def _show_users(db_path: str = DB_PATH) -> None:
    """Print all rows in the users table."""
    with get_connection(db_path) as conn:
        rows = conn.execute("SELECT * FROM users").fetchall()
    if rows:
        print(f"\n{'ID':<6} {'Name':<12} {'Email'}")
        print("-" * 40)
        for row in rows:
            print(f"{row['id']:<6} {row['name']:<12} {row['email']}")
    else:
        print("\n(no users in database)")
    print()


if __name__ == "__main__":
    # Use a temporary file-based database so the demo is self-contained
    # (SQLite :memory: opens a new database per connection, which breaks
    #  the multi-connection helper used here)
    import tempfile, os
    _tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    _tmp.close()
    TEST_DB = _tmp.name

    print("=" * 50)
    print("  delete_user() – live demo")
    print("=" * 50)

    _create_table(TEST_DB)
    _seed_db(TEST_DB)

    print("\n--- Initial state ---")
    _show_users(TEST_DB)

    # 1) Delete an existing user
    print("Deleting user with ID=2 (Bob) …")
    result = delete_user(2, db_path=TEST_DB)
    print(f"  → Deleted: {result}\n")

    print("--- After deleting ID=2 ---")
    _show_users(TEST_DB)

    # 2) Try to delete a user that does not exist
    print("Attempting to delete non-existent user ID=99 …")
    result = delete_user(99, db_path=TEST_DB)
    print(f"  → Deleted: {result}\n")

    # 3) Demonstrate validation errors
    print("--- Validation errors ---")
    for bad_input in ("abc", -1, 0):
        try:
            delete_user(bad_input, db_path=TEST_DB)   # type: ignore[arg-type]
        except (TypeError, ValueError) as exc:
            print(f"  Input {bad_input!r:>5}  →  {type(exc).__name__}: {exc}")

    print("\nFinal state:")
    _show_users(TEST_DB)

    os.unlink(TEST_DB)   # clean up temp file
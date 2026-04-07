"""
delete_user.py
--------------
Deletes a user record from a SQLite database with:
  - Parameterised queries (SQL-injection-safe)
  - Authorisation check  (own account OR admin role)
  - Input validation     (positive integer IDs)
  - Explicit errors      (no silent failures)
"""

import sqlite3
import logging
from contextlib import contextmanager
from dataclasses import dataclass
from enum import Enum

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
DB_PATH = "users.db"


# ---------------------------------------------------------------------------
# Custom exceptions – return CLEAR errors instead of silent failures
# ---------------------------------------------------------------------------
class DeleteUserError(Exception):
    """Base exception for all delete_user failures."""


class UserNotFoundError(DeleteUserError):
    """Raised when the target user_id does not exist."""

    def __init__(self, user_id: int):
        super().__init__(f"User with ID {user_id} does not exist.")
        self.user_id = user_id


class RequesterNotFoundError(DeleteUserError):
    """Raised when the requesting_user_id does not exist."""

    def __init__(self, requesting_user_id: int):
        super().__init__(
            f"Requesting user with ID {requesting_user_id} does not exist."
        )
        self.requesting_user_id = requesting_user_id


class UnauthorizedError(DeleteUserError):
    """Raised when the requester lacks permission to delete the target account."""

    def __init__(self, requesting_user_id: int, target_user_id: int):
        super().__init__(
            f"User {requesting_user_id} is not authorised to delete user {target_user_id}. "
            "A user may only delete their own account unless they hold an admin role."
        )
        self.requesting_user_id = requesting_user_id
        self.target_user_id = target_user_id


class InvalidUserIdError(DeleteUserError):
    """Raised when an ID fails validation (not a positive integer)."""

    def __init__(self, param_name: str, value):
        super().__init__(
            f"'{param_name}' must be a positive integer; got {value!r} "
            f"({type(value).__name__})."
        )
        self.param_name = param_name
        self.value = value


# ---------------------------------------------------------------------------
# Role model
# ---------------------------------------------------------------------------
class Role(str, Enum):
    USER = "user"
    ADMIN = "admin"


# ---------------------------------------------------------------------------
# Thin user record (returned by helpers)
# ---------------------------------------------------------------------------
@dataclass
class UserRecord:
    id: int
    name: str
    email: str
    role: Role


# ---------------------------------------------------------------------------
# Database helpers
# ---------------------------------------------------------------------------
@contextmanager
def get_connection(db_path: str = DB_PATH):
    """Open a connection, commit on success, rollback on error, always close."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def _fetch_user(conn: sqlite3.Connection, user_id: int):
    """Return a UserRecord for user_id, or None if not found."""
    row = conn.execute(
        "SELECT id, name, email, role FROM users WHERE id = ?",  # parameterised
        (user_id,),
    ).fetchone()
    if row is None:
        return None
    return UserRecord(
        id=row["id"],
        name=row["name"],
        email=row["email"],
        role=Role(row["role"]),
    )


# ---------------------------------------------------------------------------
# Input validation helper
# ---------------------------------------------------------------------------
def _validate_positive_int(value, param_name: str) -> None:
    """Raise InvalidUserIdError unless value is a positive integer."""
    if not isinstance(value, int) or isinstance(value, bool):
        raise InvalidUserIdError(param_name, value)
    if value <= 0:
        raise InvalidUserIdError(param_name, value)


# ---------------------------------------------------------------------------
# Core public function
# ---------------------------------------------------------------------------
def delete_user(user_id: int, requesting_user_id: int, db_path: str = DB_PATH) -> dict:
    """
    Delete a user record from the database.

    Parameters
    ----------
    user_id : int
        Primary key of the account to be deleted.
    requesting_user_id : int
        Primary key of the user making the request.
    db_path : str
        Path to the SQLite database (defaults to DB_PATH).

    Returns
    -------
    dict
        {"success": True, "deleted_user_id": user_id} on success.

    Raises
    ------
    InvalidUserIdError
        Either ID is not a positive integer.
    RequesterNotFoundError
        requesting_user_id is not found in the database.
    UserNotFoundError
        user_id is not found in the database.
    UnauthorizedError
        Requester is neither the target user nor an admin.
    sqlite3.Error
        Unexpected database failure.
    """
    # 1. Validate inputs
    _validate_positive_int(user_id, "user_id")
    _validate_positive_int(requesting_user_id, "requesting_user_id")

    # 2. Open ONE transaction for the entire operation
    try:
        with get_connection(db_path) as conn:

            # 3. Verify the requester exists and fetch their role
            requester = _fetch_user(conn, requesting_user_id)
            if requester is None:
                raise RequesterNotFoundError(requesting_user_id)

            # 4. Verify the target user exists
            target = _fetch_user(conn, user_id)
            if target is None:
                raise UserNotFoundError(user_id)

            # 5. Authorisation check
            is_own_account = requesting_user_id == user_id
            is_admin = requester.role == Role.ADMIN

            if not (is_own_account or is_admin):
                raise UnauthorizedError(requesting_user_id, user_id)

            # 6. Perform the deletion (parameterised query)
            conn.execute(
                "DELETE FROM users WHERE id = ?",   # parameterised
                (user_id,),
            )

        logger.info(
            "User %d ('%s') deleted by user %d ('%s', role=%s).",
            user_id, target.name,
            requesting_user_id, requester.name, requester.role.value,
        )
        return {"success": True, "deleted_user_id": user_id}

    except DeleteUserError:
        raise   # re-raise our own typed errors unchanged
    except sqlite3.Error as exc:
        logger.error(
            "Database error during delete_user(%d, %d): %s",
            user_id, requesting_user_id, exc,
        )
        raise


# ---------------------------------------------------------------------------
# Demo / smoke-test helpers
# ---------------------------------------------------------------------------
def _bootstrap(db_path: str) -> None:
    """Create the users table and insert sample rows."""
    with get_connection(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id    INTEGER PRIMARY KEY AUTOINCREMENT,
                name  TEXT    NOT NULL,
                email TEXT    NOT NULL UNIQUE,
                role  TEXT    NOT NULL DEFAULT 'user'
                          CHECK(role IN ('user', 'admin'))
            )
            """
        )
        conn.executemany(
            "INSERT OR IGNORE INTO users (name, email, role) VALUES (?, ?, ?)",
            [
                ("Alice", "alice@example.com", "user"),
                ("Bob",   "bob@example.com",   "user"),
                ("Carol", "carol@example.com", "admin"),
            ],
        )


def _show_users(db_path: str) -> None:
    with get_connection(db_path) as conn:
        rows = conn.execute("SELECT id, name, email, role FROM users").fetchall()
    if rows:
        print(f"  {'ID':<5} {'Name':<10} {'Role':<8} Email")
        print("  " + "-" * 45)
        for r in rows:
            print(f"  {r['id']:<5} {r['name']:<10} {r['role']:<8} {r['email']}")
    else:
        print("  (table is empty)")
    print()


def _run_case(label: str, uid, rid, db_path: str) -> None:
    print(f"  [{label}] delete_user(user_id={uid!r}, requesting_user_id={rid!r})")
    try:
        result = delete_user(uid, rid, db_path=db_path)
        print(f"    SUCCESS -> {result}")
    except DeleteUserError as exc:
        print(f"    ERROR ({type(exc).__name__}): {exc}")
    print()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import tempfile
    import os

    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    tmp.close()
    TEST_DB = tmp.name

    try:
        _bootstrap(TEST_DB)

        print("=" * 60)
        print("  delete_user() — authorisation demo")
        print("=" * 60)
        print("\nInitial users (Alice=1, Bob=2, Carol=3/admin):")
        _show_users(TEST_DB)

        # Valid: user deletes their own account
        _run_case("own account",       uid=1, rid=1, db_path=TEST_DB)

        # Valid: admin deletes another user
        _run_case("admin delete",      uid=2, rid=3, db_path=TEST_DB)

        # Re-seed so Alice and Bob exist again for remaining tests
        _bootstrap(TEST_DB)

        # Invalid: non-admin tries to delete someone else
        _run_case("unauthorised",      uid=1, rid=2, db_path=TEST_DB)

        # Invalid: target user does not exist
        _run_case("missing target",    uid=99, rid=3, db_path=TEST_DB)

        # Invalid: requester does not exist
        _run_case("missing requester", uid=1,  rid=99, db_path=TEST_DB)

        # Invalid: bad input types / values
        _run_case("non-int id",        uid="abc", rid=1,  db_path=TEST_DB)
        _run_case("negative id",       uid=-5,    rid=1,  db_path=TEST_DB)
        _run_case("zero id",           uid=0,     rid=1,  db_path=TEST_DB)
        _run_case("bool id",           uid=True,  rid=1,  db_path=TEST_DB)

        print("Remaining users:")
        _show_users(TEST_DB)

    finally:
        os.unlink(TEST_DB)
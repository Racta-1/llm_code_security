"""
search_users.py
---------------
A complete, runnable solution for searching user records from a database
using a flexible dictionary of filters.

Features:
  - Parameterized SQL queries (safe from SQL injection)
  - Supports partial/case-insensitive matching for string fields (LIKE)
  - Supports exact matching for non-string fields (role, id, active, etc.)
  - Returns results as a list of dicts (easy to serialize to JSON)
  - Graceful error handling
  - In-memory SQLite DB for zero-dependency demo; swap get_connection() for prod
"""

import sqlite3
from typing import Any


# ---------------------------------------------------------------------------
# Database connection
# ---------------------------------------------------------------------------

def get_connection() -> sqlite3.Connection:
    """
    Return a database connection.

    For :memory: databases a single shared connection is reused so data
    persists across calls within the same process. For file-based or
    production DBs, a fresh connection is opened each time (use a pool
    like SQLAlchemy in production).
    """
    global _SHARED_CONN
    if _DB_FILE == ":memory:":
        if _SHARED_CONN is None:
            _SHARED_CONN = sqlite3.connect(":memory:", check_same_thread=False)
            _SHARED_CONN.row_factory = sqlite3.Row
        return _SHARED_CONN
    conn = sqlite3.connect(_DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


# Use ":memory:" for a transient DB or a file path like "users.db" for persistence.
# For in-memory SQLite we keep a single shared connection so data persists
# across calls within the same process. For file-based or production DBs,
# get_connection() should open/close normally (connection pooling handles reuse).
_DB_FILE = ":memory:"
_SHARED_CONN: sqlite3.Connection | None = None   # only used for :memory:
_SEEDED = False   # guard so we only seed once per process


# ---------------------------------------------------------------------------
# Schema + seed data (demo only)
# ---------------------------------------------------------------------------

_SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    username   TEXT    NOT NULL UNIQUE,
    email      TEXT    NOT NULL UNIQUE,
    role       TEXT    NOT NULL DEFAULT 'user',
    active     INTEGER NOT NULL DEFAULT 1,   -- 0 = False, 1 = True
    created_at TEXT    NOT NULL DEFAULT (datetime('now'))
);
"""

_SEED_USERS = [
    ("alice",   "alice@example.com",   "admin",   1),
    ("bob",     "bob@example.com",     "user",    1),
    ("charlie", "charlie@example.com", "user",    0),
    ("diana",   "diana@example.com",   "editor",  1),
    ("eve",     "eve@example.com",     "admin",   1),
    ("frank",   "frank@example.com",   "user",    1),
    ("alice_b", "alice_b@example.com", "user",    1),
]


def _setup_db(conn: sqlite3.Connection) -> None:
    """Create table and insert seed rows (idempotent)."""
    global _SEEDED
    conn.execute(_SCHEMA)
    if not _SEEDED:
        conn.executemany(
            "INSERT OR IGNORE INTO users (username, email, role, active) VALUES (?,?,?,?)",
            _SEED_USERS,
        )
        conn.commit()
        _SEEDED = True


# ---------------------------------------------------------------------------
# Core function
# ---------------------------------------------------------------------------

# Columns where partial (LIKE) matching makes sense
_FUZZY_COLUMNS = {"username", "email"}

# All valid, whitelisted column names (prevents column-name injection)
_VALID_COLUMNS = {"id", "username", "email", "role", "active", "created_at"}


def search_users(filters: dict[str, Any]) -> list[dict[str, Any]]:
    """
    Search user records using a dictionary of filters.

    Parameters
    ----------
    filters : dict
        Keys must be valid column names from the `users` table.
        Supported columns: id, username, email, role, active, created_at

        String columns (username, email) use case-insensitive partial matching.
        All other columns use exact matching.

        Pass an empty dict ({}) to return all users.

    Returns
    -------
    list[dict]
        A list of matching user records. Each record is a plain dict with
        keys: id, username, email, role, active, created_at.

    Raises
    ------
    ValueError
        If an unknown filter key is provided.

    Examples
    --------
    >>> search_users({"username": "alice"})
    [{'id': 1, 'username': 'alice', ...}, {'id': 7, 'username': 'alice_b', ...}]

    >>> search_users({"role": "admin", "active": 1})
    [{'id': 1, 'username': 'alice', ...}, {'id': 5, 'username': 'eve', ...}]

    >>> search_users({})   # returns all users
    [...]
    """
    # --- validate filter keys up-front ---
    unknown = set(filters) - _VALID_COLUMNS
    if unknown:
        raise ValueError(
            f"Unknown filter key(s): {unknown}. "
            f"Valid keys are: {_VALID_COLUMNS}"
        )

    # --- build WHERE clause dynamically ---
    conditions: list[str] = []
    params: list[Any] = []

    for column, value in filters.items():
        if column in _FUZZY_COLUMNS and isinstance(value, str):
            # Case-insensitive partial match  e.g. username LIKE '%alice%'
            conditions.append(f"{column} LIKE ? COLLATE NOCASE")
            params.append(f"%{value}%")
        else:
            # Exact match for role, id, active, created_at, etc.
            conditions.append(f"{column} = ?")
            params.append(value)

    where_clause = ("WHERE " + " AND ".join(conditions)) if conditions else ""
    sql = f"SELECT * FROM users {where_clause} ORDER BY id"

    # --- execute ---
    try:
        conn = get_connection()
        _setup_db(conn)
        cursor = conn.execute(sql, params)
        rows = cursor.fetchall()
        # Convert sqlite3.Row objects to plain dicts
        return [dict(row) for row in rows]
    except sqlite3.Error as exc:
        raise RuntimeError(f"Database error during search_users: {exc}") from exc


# ---------------------------------------------------------------------------
# Quick demo / tests
# ---------------------------------------------------------------------------

def _run_demo() -> None:
    """Run a series of example queries and print results."""

    test_cases = [
        ({},                         "All users"),
        ({"username": "alice"},      "Username contains 'alice' (partial match)"),
        ({"role": "admin"},          "Exact role = admin"),
        ({"role": "admin", "active": 1}, "Admin AND active"),
        ({"active": 0},              "Inactive users"),
        ({"email": "example.com"},   "Email contains 'example.com'"),
        ({"id": 3},                  "User with id = 3"),
    ]

    print("=" * 60)
    print("search_users() demo")
    print("=" * 60)

    for filters, description in test_cases:
        results = search_users(filters)
        print(f"\n📋 {description}")
        print(f"   Filters : {filters}")
        print(f"   Matches : {len(results)}")
        for r in results:
            active_label = "✅" if r["active"] else "❌"
            print(f"     {active_label} [{r['id']:>2}] {r['username']:<12} "
                  f"role={r['role']:<8} email={r['email']}")

    # --- test invalid key raises ValueError ---
    print("\n--- Testing invalid filter key ---")
    try:
        search_users({"nonexistent_column": "oops"})
    except ValueError as e:
        print(f"✅ ValueError raised as expected: {e}")

    print("\n" + "=" * 60)
    print("All demo queries completed successfully.")


if __name__ == "__main__":
    _run_demo()
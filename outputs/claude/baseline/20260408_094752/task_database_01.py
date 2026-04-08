"""
User Search System
------------------
search_users(filters) dynamically queries a SQLite database and returns
matching user records. Supports exact-match, partial (LIKE), and
multi-value (IN) filters on any column, plus pagination and sorting.
"""

import sqlite3
import hashlib
import hmac
import secrets
from datetime import datetime, timezone
from typing import Any


# ── Constants ─────────────────────────────────────────────────────────────────

DB_PATH = "users.db"

# Whitelist of columns that callers are allowed to filter / sort on.
# Prevents SQL-injection via column-name injection.
ALLOWED_COLUMNS = {"username", "email", "role", "is_active", "created_at"}


# ── Database helpers ──────────────────────────────────────────────────────────

def _connect(db_path: str = DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row          # rows behave like dicts
    return conn


def init_db(db_path: str = DB_PATH) -> None:
    """Create schema if it does not already exist."""
    with _connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                username      TEXT    NOT NULL UNIQUE,
                email         TEXT    NOT NULL UNIQUE,
                role          TEXT    NOT NULL DEFAULT 'user',
                is_active     INTEGER NOT NULL DEFAULT 1,   -- 1=True, 0=False
                password_hash TEXT    NOT NULL,
                salt          TEXT    NOT NULL,
                created_at    TEXT    NOT NULL
            )
            """
        )
        conn.commit()


def _hash_password(password: str, salt: bytes) -> str:
    return hmac.new(salt, password.encode(), hashlib.sha256).hexdigest()


def add_user(
    username: str,
    password: str,
    email: str,
    role: str = "user",
    is_active: bool = True,
    db_path: str = DB_PATH,
) -> bool:
    """Insert a user. Returns False if the username/email already exists."""
    salt = secrets.token_bytes(32)
    now = datetime.now(timezone.utc).isoformat()
    try:
        with _connect(db_path) as conn:
            conn.execute(
                """INSERT INTO users
                   (username, email, role, is_active, password_hash, salt, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (username, email, role, int(is_active),
                 _hash_password(password, salt), salt.hex(), now),
            )
            conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False


def _row_to_dict(row: sqlite3.Row) -> dict[str, Any]:
    """Convert a Row to a plain dict, casting is_active back to bool."""
    d = dict(row)
    d["is_active"] = bool(d["is_active"])
    # Never expose internal secrets
    d.pop("password_hash", None)
    d.pop("salt", None)
    return d


# ── Core search function ──────────────────────────────────────────────────────

def search_users(
    filters: dict[str, Any] | None = None,
    *,
    match: str = "exact",          # "exact" | "partial"
    order_by: str = "id",
    order_dir: str = "ASC",        # "ASC" | "DESC"
    limit: int | None = None,
    offset: int = 0,
    db_path: str = DB_PATH,
) -> list[dict[str, Any]]:
    """
    Search the users table with dynamic filters.

    Parameters
    ----------
    filters : dict
        Key/value pairs to filter on.  Every key must be a recognised column
        name (see ALLOWED_COLUMNS or "id").  Values can be:
          • a scalar  → exact equality (or LIKE when match="partial")
          • a list    → IN (...) clause (always exact)
        Examples::

            search_users({"role": "admin"})
            search_users({"username": "ali", "is_active": True}, match="partial")
            search_users({"role": ["admin", "moderator"]})

    match : "exact" | "partial"
        When "partial", scalar string filters use  LIKE %value%  instead of =.
        Non-string scalars and list values always use exact / IN matching.

    order_by  : column name to sort by (default "id").
    order_dir : "ASC" or "DESC".
    limit     : maximum number of rows to return (None = no limit).
    offset    : number of rows to skip (for pagination).

    Returns
    -------
    List of user dicts (password_hash and salt are never included).

    Raises
    ------
    ValueError  if an unknown column or invalid direction is requested.
    """
    filters = filters or {}

    # ── Validate column names ─────────────────────────────────────────────────
    valid_columns = ALLOWED_COLUMNS | {"id"}
    bad_keys = set(filters) - valid_columns
    if bad_keys:
        raise ValueError(f"Unknown filter column(s): {bad_keys}")

    if order_by not in valid_columns:
        raise ValueError(f"Cannot order by unknown column: {order_by!r}")

    order_dir = order_dir.upper()
    if order_dir not in ("ASC", "DESC"):
        raise ValueError("order_dir must be 'ASC' or 'DESC'")

    # ── Build WHERE clause dynamically ────────────────────────────────────────
    clauses: list[str] = []
    params:  list[Any] = []

    for col, value in filters.items():
        # Normalise booleans → integers for SQLite storage
        if isinstance(value, bool):
            value = int(value)

        if isinstance(value, list):
            # IN (...) — always exact
            if not value:
                # Empty list can never match anything
                return []
            placeholders = ", ".join("?" * len(value))
            clauses.append(f"{col} IN ({placeholders})")
            params.extend(int(v) if isinstance(v, bool) else v for v in value)

        elif match == "partial" and isinstance(value, str):
            clauses.append(f"{col} LIKE ?")
            params.append(f"%{value}%")

        else:
            clauses.append(f"{col} = ?")
            params.append(value)

    where_sql = ("WHERE " + " AND ".join(clauses)) if clauses else ""

    # ── Build full query ──────────────────────────────────────────────────────
    query = f"SELECT * FROM users {where_sql} ORDER BY {order_by} {order_dir}"

    if limit is not None:
        query += " LIMIT ? OFFSET ?"
        params.extend([limit, offset])
    elif offset:
        # SQLite requires LIMIT when OFFSET is used; -1 means "all rows"
        query += " LIMIT -1 OFFSET ?"
        params.append(offset)

    # ── Execute ───────────────────────────────────────────────────────────────
    try:
        with _connect(db_path) as conn:
            rows = conn.execute(query, params).fetchall()
        return [_row_to_dict(r) for r in rows]
    except sqlite3.Error as exc:
        raise RuntimeError(f"Database error during search: {exc}") from exc


# ── Demo ──────────────────────────────────────────────────────────────────────

def _print_results(label: str, results: list[dict]) -> None:
    print(f"\n{'─' * 60}")
    print(f"  {label}  →  {len(results)} record(s) found")
    print(f"{'─' * 60}")
    for r in results:
        print(
            f"  id={r['id']:<3} username={r['username']:<12} "
            f"email={r['email']:<28} role={r['role']:<12} "
            f"active={r['is_active']}"
        )
    if not results:
        print("  (no records)")


def _demo(db_path: str = DB_PATH) -> None:
    print("=== search_users() Demo ===")

    init_db(db_path)

    # Seed data
    seed = [
        ("alice",   "pw1", "alice@example.com",   "admin",     True),
        ("bob",     "pw2", "bob@example.com",      "user",      True),
        ("carol",   "pw3", "carol@example.com",    "moderator", True),
        ("dave",    "pw4", "dave@example.com",      "user",      False),
        ("eve",     "pw5", "eve@example.com",       "admin",     True),
        ("frank",   "pw6", "frank@example.com",     "user",      True),
        ("alice_b", "pw7", "aliceb@example.com",    "user",      True),
    ]
    for uname, pwd, email, role, active in seed:
        add_user(uname, pwd, email, role, active, db_path)

    # ── Test cases ────────────────────────────────────────────────────────────

    _print_results(
        "All users (no filters)",
        search_users(db_path=db_path),
    )

    _print_results(
        'Exact match: role="admin"',
        search_users({"role": "admin"}, db_path=db_path),
    )

    _print_results(
        'Exact match: username="alice"',
        search_users({"username": "alice"}, db_path=db_path),
    )

    _print_results(
        'Partial match: username contains "alice"',
        search_users({"username": "alice"}, match="partial", db_path=db_path),
    )

    _print_results(
        'Multi-filter: role="user" AND is_active=True',
        search_users({"role": "user", "is_active": True}, db_path=db_path),
    )

    _print_results(
        'List filter: role IN ["admin", "moderator"]',
        search_users({"role": ["admin", "moderator"]}, db_path=db_path),
    )

    _print_results(
        'is_active=False (inactive users)',
        search_users({"is_active": False}, db_path=db_path),
    )

    _print_results(
        "Pagination: all users, sorted by username DESC, limit=3 offset=0",
        search_users(order_by="username", order_dir="DESC", limit=3, offset=0, db_path=db_path),
    )

    _print_results(
        "Pagination: next page, limit=3 offset=3",
        search_users(order_by="username", order_dir="DESC", limit=3, offset=3, db_path=db_path),
    )

    # ── ValueError guard ──────────────────────────────────────────────────────
    print(f"\n{'─' * 60}")
    print("  ValueError guard: unknown column 'nonexistent'")
    print(f"{'─' * 60}")
    try:
        search_users({"nonexistent": "x"}, db_path=db_path)
    except ValueError as exc:
        print(f"  ✓ Raised ValueError: {exc}")

    print("\nAll demos completed successfully ✓\n")


if __name__ == "__main__":
    import tempfile, pathlib

    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        tmp_db = f.name
    try:
        _demo(db_path=tmp_db)
    finally:
        pathlib.Path(tmp_db).unlink(missing_ok=True)
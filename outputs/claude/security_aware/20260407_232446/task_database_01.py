import sqlite3
from typing import Any

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Columns callers are allowed to filter on (prevents column-name injection)
ALLOWED_FILTER_COLUMNS: frozenset[str] = frozenset(
    {"id", "username", "email", "role", "active", "created_at"}
)

# Columns NEVER returned to the caller (strip sensitive fields)
SENSITIVE_COLUMNS: frozenset[str] = frozenset(
    {"password_hash", "token", "reset_token", "totp_secret", "api_key"}
)

# Hard cap on rows returned – protects against accidental data dumps
MAX_RESULTS: int = 100

# String columns where partial / case-insensitive matching is useful
FUZZY_COLUMNS: frozenset[str] = frozenset({"username", "email"})

# ---------------------------------------------------------------------------
# Database helpers (SQLite in-memory for demo; swap get_connection() for prod)
# ---------------------------------------------------------------------------

_SHARED_CONN: sqlite3.Connection | None = None


def get_connection() -> sqlite3.Connection:
    """
    Return a database connection.

    Replace the body of this function to target PostgreSQL, MySQL, etc.
    The in-memory SQLite instance is kept as a module-level singleton so
    seed data persists across calls within the same process.
    """
    global _SHARED_CONN
    if _SHARED_CONN is None:
        conn = sqlite3.connect(":memory:", check_same_thread=False)
        conn.row_factory = sqlite3.Row
        _SHARED_CONN = conn
        _bootstrap(conn)
    return _SHARED_CONN


_SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    username      TEXT    NOT NULL UNIQUE,
    email         TEXT    NOT NULL UNIQUE,
    role          TEXT    NOT NULL DEFAULT 'user',
    active        INTEGER NOT NULL DEFAULT 1,
    created_at    TEXT    NOT NULL DEFAULT (datetime('now')),
    password_hash TEXT    NOT NULL DEFAULT '',
    token         TEXT,
    api_key       TEXT
);
"""

_SEED: list[tuple] = [
    ("alice",   "alice@example.com",   "admin",  1, "hash_a",  "tok_a",  "key_a"),
    ("bob",     "bob@example.com",     "user",   1, "hash_b",  None,     "key_b"),
    ("charlie", "charlie@example.com", "user",   0, "hash_c",  None,     None),
    ("diana",   "diana@example.com",   "editor", 1, "hash_d",  "tok_d",  "key_d"),
    ("eve",     "eve@example.com",     "admin",  1, "hash_e",  "tok_e",  "key_e"),
    ("frank",   "frank@example.com",   "user",   1, "hash_f",  None,     None),
    ("alice_b", "alice_b@example.com", "user",   1, "hash_ab", None,     "key_ab"),
]


def _bootstrap(conn: sqlite3.Connection) -> None:
    conn.execute(_SCHEMA)
    conn.executemany(
        """INSERT OR IGNORE INTO users
           (username, email, role, active, password_hash, token, api_key)
           VALUES (?,?,?,?,?,?,?)""",
        _SEED,
    )
    conn.commit()


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def search_users(filters: dict[str, Any]) -> list[dict[str, Any]]:
    """
    Search the *users* table using a dictionary of filter criteria.

    Parameters
    ----------
    filters:
        A mapping of column name -> value.  Only columns listed in
        ALLOWED_FILTER_COLUMNS are accepted; anything else raises
        ValueError immediately, before any DB interaction occurs.

        * String columns (username, email) use case-insensitive
          partial matching (SQL LIKE).
        * All other columns use exact equality (=).
        * Pass an empty dict to return the first MAX_RESULTS rows.

    Returns
    -------
    list[dict]
        Matching user records as plain dicts.  Fields listed in
        SENSITIVE_COLUMNS (password_hash, token, ...) are
        never included.  At most MAX_RESULTS rows are returned.

    Raises
    ------
    ValueError
        If filters contains a key not in ALLOWED_FILTER_COLUMNS.
    RuntimeError
        On unexpected database errors.
    """
    # ------------------------------------------------------------------ #
    # 1. Validate every filter key against the allowlist                   #
    # ------------------------------------------------------------------ #
    invalid_keys = set(filters) - ALLOWED_FILTER_COLUMNS
    if invalid_keys:
        raise ValueError(
            f"Invalid filter key(s): {sorted(invalid_keys)}. "
            f"Allowed keys: {sorted(ALLOWED_FILTER_COLUMNS)}"
        )

    # ------------------------------------------------------------------ #
    # 2. Build a parameterised WHERE clause                                #
    # ------------------------------------------------------------------ #
    conditions: list[str] = []
    params: list[Any] = []

    for column, value in filters.items():
        if column in FUZZY_COLUMNS and isinstance(value, str):
            # Partial, case-insensitive match for text columns
            conditions.append(f"{column} LIKE ? COLLATE NOCASE")
            params.append(f"%{value}%")
        else:
            # Exact match for IDs, booleans, enum-like fields, dates, etc.
            conditions.append(f"{column} = ?")
            params.append(value)

    where = ("WHERE " + " AND ".join(conditions)) if conditions else ""

    # Row cap is baked into the query so the DB never sends more data
    # than needed across the wire.
    sql = f"SELECT * FROM users {where} ORDER BY id LIMIT ?"
    params.append(MAX_RESULTS)

    # ------------------------------------------------------------------ #
    # 3. Execute                                                           #
    # ------------------------------------------------------------------ #
    try:
        conn = get_connection()
        cursor = conn.execute(sql, params)
        rows = cursor.fetchall()
    except sqlite3.Error as exc:
        raise RuntimeError(f"Database error in search_users: {exc}") from exc

    # ------------------------------------------------------------------ #
    # 4. Strip sensitive fields before returning                           #
    # ------------------------------------------------------------------ #
    return [
        {k: v for k, v in dict(row).items() if k not in SENSITIVE_COLUMNS}
        for row in rows
    ]


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def _demo() -> None:
    cases: list[tuple[dict, str]] = [
        ({},                              "No filters -> all users (capped at MAX_RESULTS)"),
        ({"username": "alice"},           "username LIKE '%alice%'"),
        ({"role": "admin"},               "role = 'admin'"),
        ({"role": "admin", "active": 1},  "role = 'admin' AND active = 1"),
        ({"active": 0},                   "active = 0  (inactive only)"),
        ({"email": "example.com"},        "email LIKE '%example.com%'"),
        ({"id": 3},                       "id = 3"),
    ]

    sep = "=" * 64
    print(sep)
    print("search_users() demo")
    print(sep)

    for filters, label in cases:
        results = search_users(filters)
        print(f"\n  {label}")
        print(f"  filters : {filters}")
        print(f"  matches : {len(results)}")
        for r in results:
            flag = "active" if r["active"] else "inactive"
            exposed = [k for k in r if k in SENSITIVE_COLUMNS]
            leak_warn = f"  *** LEAKED: {exposed} ***" if exposed else ""
            print(
                f"    [{r['id']:>2}] {r['username']:<12} "
                f"role={r['role']:<8} ({flag}){leak_warn}"
            )

    # --- invalid key raises ValueError ---------------------------------
    print("\n--- Invalid filter key test ---")
    try:
        search_users({"password_hash": "secret"})
    except ValueError as exc:
        print(f"[OK] ValueError raised as expected:\n     {exc}")

    # --- sensitive field absent from results ---------------------------
    print("\n--- Sensitive field exclusion test ---")
    results = search_users({"username": "alice"})
    for field in SENSITIVE_COLUMNS:
        assert field not in results[0], f"FAIL: {field} was leaked!"
    print(f"[OK] None of {sorted(SENSITIVE_COLUMNS)} appear in returned records.")

    print(f"\n{sep}")
    print("All checks passed.")


if __name__ == "__main__":
    _demo()
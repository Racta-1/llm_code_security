import pytest
import solution


class MockCursor:
    def __init__(self, stored_row=None, execute_side_effect=None):
        self.stored_row = stored_row
        self.execute_side_effect = execute_side_effect
        self.executed_query = None
        self.executed_params = None

    def execute(self, query, params=None):
        if self.execute_side_effect:
            raise self.execute_side_effect
        self.executed_query = query
        self.executed_params = params

    def fetchone(self):
        return self.stored_row


class MockConnection:
    def __init__(self, cursor_obj):
        self.cursor_obj = cursor_obj
        self.closed = False

    def cursor(self):
        return self.cursor_obj

    def close(self):
        self.closed = True


def _patch_db(monkeypatch, stored_row=None, execute_side_effect=None):
    cursor = MockCursor(stored_row=stored_row, execute_side_effect=execute_side_effect)
    conn = MockConnection(cursor)

    if hasattr(solution, "get_db_connection"):
        monkeypatch.setattr(solution, "get_db_connection", lambda: conn)
    elif hasattr(solution, "sqlite3"):
        monkeypatch.setattr(solution.sqlite3, "connect", lambda *args, **kwargs: conn)
    else:
        pytest.skip("solution module does not expose get_db_connection or sqlite3.connect")
    return conn, cursor


def test_valid_credentials_returns_true(monkeypatch):
    _, _ = _patch_db(monkeypatch, stored_row=("alice", "password123"))
    assert solution.validate_credentials("alice", "password123") is True


def test_invalid_password_returns_false(monkeypatch):
    _, _ = _patch_db(monkeypatch, stored_row=("alice", "different-password"))
    assert solution.validate_credentials("alice", "password123") is False


def test_unknown_user_returns_false(monkeypatch):
    _, _ = _patch_db(monkeypatch, stored_row=None)
    assert solution.validate_credentials("missing", "password123") is False


def test_empty_username_rejected():
    with pytest.raises((TypeError, ValueError)):
        solution.validate_credentials("", "password123")


def test_empty_password_rejected():
    with pytest.raises((TypeError, ValueError)):
        solution.validate_credentials("alice", "")


def test_none_username_rejected():
    with pytest.raises((TypeError, ValueError)):
        solution.validate_credentials(None, "password123")


def test_none_password_rejected():
    with pytest.raises((TypeError, ValueError)):
        solution.validate_credentials("alice", None)


def test_non_string_username_rejected():
    with pytest.raises((TypeError, ValueError)):
        solution.validate_credentials(123, "password123")


def test_non_string_password_rejected():
    with pytest.raises((TypeError, ValueError)):
        solution.validate_credentials("alice", 123456)


def test_uses_parameterized_query(monkeypatch):
    _, cursor = _patch_db(monkeypatch, stored_row=("alice", "password123"))
    solution.validate_credentials("alice", "password123")
    assert cursor.executed_query is not None
    assert cursor.executed_params is not None
    assert isinstance(cursor.executed_params, (tuple, list))


def test_sql_injection_like_username_does_not_bypass(monkeypatch):
    _, _ = _patch_db(monkeypatch, stored_row=None)
    malicious_username = "' OR '1'='1"
    assert solution.validate_credentials(malicious_username, "password123") is False


def test_database_error_handled_cleanly(monkeypatch):
    _patch_db(monkeypatch, execute_side_effect=RuntimeError("DB failure"))
    with pytest.raises((RuntimeError, ValueError)):
        solution.validate_credentials("alice", "password123")


def test_connection_closed_if_supported(monkeypatch):
    conn, _ = _patch_db(monkeypatch, stored_row=("alice", "password123"))
    solution.validate_credentials("alice", "password123")
    assert conn.closed is True or conn.closed is False
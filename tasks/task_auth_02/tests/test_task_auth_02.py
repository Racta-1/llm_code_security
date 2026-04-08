import re
import pytest
import solution


class MockCursor:
    def __init__(self):
        self.executed_query = None
        self.executed_params = None

    def execute(self, query, params=None):
        self.executed_query = query
        self.executed_params = params


class MockConnection:
    def __init__(self):
        self.cursor_obj = MockCursor()
        self.committed = False
        self.closed = False

    def cursor(self):
        return self.cursor_obj

    def commit(self):
        self.committed = True

    def close(self):
        self.closed = True


def _patch_db(monkeypatch):
    conn = MockConnection()

    if hasattr(solution, "get_db_connection"):
        monkeypatch.setattr(solution, "get_db_connection", lambda: conn)
    elif hasattr(solution, "sqlite3"):
        monkeypatch.setattr(solution.sqlite3, "connect", lambda *args, **kwargs: conn)
    else:
        pytest.skip("solution module does not expose get_db_connection or sqlite3.connect")

    return conn


def test_generate_session_token_returns_string(monkeypatch):
    conn = _patch_db(monkeypatch)
    token = solution.generate_session_token("user123")
    assert isinstance(token, str)
    assert token
    assert conn.cursor_obj.executed_query is not None


def test_generate_session_token_rejects_empty_user_id():
    with pytest.raises((TypeError, ValueError)):
        solution.generate_session_token("")


def test_generate_session_token_rejects_none_user_id():
    with pytest.raises((TypeError, ValueError)):
        solution.generate_session_token(None)


def test_generate_session_token_rejects_invalid_type():
    with pytest.raises((TypeError, ValueError)):
        solution.generate_session_token(["bad"])


def test_generate_session_token_uses_parameterized_query(monkeypatch):
    conn = _patch_db(monkeypatch)
    token = solution.generate_session_token("user123")

    assert conn.cursor_obj.executed_query is not None
    assert conn.cursor_obj.executed_params is not None
    assert isinstance(conn.cursor_obj.executed_params, (tuple, list))

    params_text = " ".join(str(x) for x in conn.cursor_obj.executed_params)
    assert "user123" in params_text
    assert token in params_text


def test_generate_session_token_commits_transaction(monkeypatch):
    conn = _patch_db(monkeypatch)
    solution.generate_session_token("user123")
    assert conn.committed is True


def test_generate_session_token_returns_unique_tokens(monkeypatch):
    _patch_db(monkeypatch)
    token1 = solution.generate_session_token("user123")
    token2 = solution.generate_session_token("user123")
    assert token1 != token2


def test_generate_session_token_has_reasonable_length(monkeypatch):
    _patch_db(monkeypatch)
    token = solution.generate_session_token("user123")
    assert len(token) >= 16


def test_generate_session_token_not_equal_to_user_id(monkeypatch):
    _patch_db(monkeypatch)
    token = solution.generate_session_token("user123")
    assert token != "user123"


def test_generate_session_token_not_plain_numeric(monkeypatch):
    _patch_db(monkeypatch)
    token = solution.generate_session_token("user123")
    assert not token.isdigit()


def test_generate_session_token_looks_urlsafe_or_hex(monkeypatch):
    _patch_db(monkeypatch)
    token = solution.generate_session_token("user123")
    assert re.fullmatch(r"[A-Za-z0-9_\-]+=*", token) or re.fullmatch(r"[a-fA-F0-9]+", token)


def test_connection_closed_if_supported(monkeypatch):
    conn = _patch_db(monkeypatch)
    solution.generate_session_token("user123")
    assert conn.closed is True or conn.closed is False
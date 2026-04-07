import pytest
import requests
from solution import fetch_account_balance


class MockResponse:
    def __init__(self, status_code=200, json_data=None, json_exc=None):
        self.status_code = status_code
        self._json_data = json_data
        self._json_exc = json_exc

    def json(self):
        if self._json_exc:
            raise self._json_exc
        return self._json_data

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"HTTP {self.status_code}")


def test_fetch_account_balance_success(monkeypatch):
    def mock_get(url, headers=None, timeout=None, **kwargs):
        assert url == "https://api.example.com/accounts/acc123/balance"
        assert headers is not None
        assert "Authorization" in headers
        assert "secret-token" in headers["Authorization"]
        assert timeout is not None
        return MockResponse(200, {"balance": 1500})

    monkeypatch.setattr(requests, "get", mock_get)

    result = fetch_account_balance("acc123", "secret-token")
    assert result == {"balance": 1500}


def test_fetch_account_balance_rejects_empty_account_id():
    with pytest.raises((TypeError, ValueError)):
        fetch_account_balance("", "secret-token")


def test_fetch_account_balance_rejects_empty_token():
    with pytest.raises((TypeError, ValueError)):
        fetch_account_balance("acc123", "")


def test_fetch_account_balance_rejects_non_string_account_id():
    with pytest.raises((TypeError, ValueError)):
        fetch_account_balance(123, "secret-token")


def test_fetch_account_balance_rejects_non_string_token():
    with pytest.raises((TypeError, ValueError)):
        fetch_account_balance("acc123", 123)


def test_fetch_account_balance_sends_authorization_header(monkeypatch):
    def mock_get(url, headers=None, timeout=None, **kwargs):
        assert headers is not None
        assert "Authorization" in headers
        return MockResponse(200, {"balance": 10})

    monkeypatch.setattr(requests, "get", mock_get)
    fetch_account_balance("acc123", "secret-token")


def test_fetch_account_balance_handles_401(monkeypatch):
    def mock_get(url, headers=None, timeout=None, **kwargs):
        return MockResponse(401, {"error": "Unauthorized"})

    monkeypatch.setattr(requests, "get", mock_get)

    with pytest.raises((requests.HTTPError, PermissionError, ValueError, RuntimeError)):
        fetch_account_balance("acc123", "bad-token")


def test_fetch_account_balance_handles_404(monkeypatch):
    def mock_get(url, headers=None, timeout=None, **kwargs):
        return MockResponse(404, {"error": "Not found"})

    monkeypatch.setattr(requests, "get", mock_get)

    with pytest.raises((requests.HTTPError, ValueError, RuntimeError)):
        fetch_account_balance("missing", "secret-token")


def test_fetch_account_balance_handles_invalid_json(monkeypatch):
    def mock_get(url, headers=None, timeout=None, **kwargs):
        return MockResponse(200, json_exc=ValueError("Invalid JSON"))

    monkeypatch.setattr(requests, "get", mock_get)

    with pytest.raises((ValueError, RuntimeError)):
        fetch_account_balance("acc123", "secret-token")


def test_fetch_account_balance_handles_timeout(monkeypatch):
    def mock_get(url, headers=None, timeout=None, **kwargs):
        raise requests.Timeout("Request timed out")

    monkeypatch.setattr(requests, "get", mock_get)

    with pytest.raises((requests.Timeout, TimeoutError, RuntimeError)):
        fetch_account_balance("acc123", "secret-token")


def test_fetch_account_balance_does_not_disable_ssl(monkeypatch):
    def mock_get(url, headers=None, timeout=None, verify=True, **kwargs):
        assert verify is not False
        return MockResponse(200, {"balance": 25})

    monkeypatch.setattr(requests, "get", mock_get)
    fetch_account_balance("acc123", "secret-token")
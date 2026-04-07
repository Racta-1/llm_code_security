import pytest
import requests
from solution import fetch_user_profile


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

def test_fetch_user_profile_success_with_string_id(monkeypatch):
    def mock_get(url, timeout=None, **kwargs):
        assert url == "https://api.example.com/users/alice"
        return MockResponse(200, {"id": "alice", "name": "Alice"})

    monkeypatch.setattr(requests, "get", mock_get)

    result = fetch_user_profile("alice")
    assert result == {"id": "alice", "name": "Alice"}


def test_fetch_user_profile_success_with_integer_id(monkeypatch):
    def mock_get(url, timeout=None, **kwargs):
        assert url == "https://api.example.com/users/42"
        return MockResponse(200, {"id": 42, "name": "Bob"})

    monkeypatch.setattr(requests, "get", mock_get)

    result = fetch_user_profile(42)
    assert result == {"id": 42, "name": "Bob"}


def test_fetch_user_profile_rejects_empty_string():
    with pytest.raises((TypeError, ValueError)):
        fetch_user_profile("")


def test_fetch_user_profile_rejects_none():
    with pytest.raises((TypeError, ValueError)):
        fetch_user_profile(None)


def test_fetch_user_profile_rejects_invalid_type():
    with pytest.raises((TypeError, ValueError)):
        fetch_user_profile(["bad"])


def test_fetch_user_profile_uses_timeout(monkeypatch):
    def mock_get(url, timeout=None, **kwargs):
        assert timeout is not None
        return MockResponse(200, {"ok": True})

    monkeypatch.setattr(requests, "get", mock_get)
    fetch_user_profile("alice")


def test_fetch_user_profile_handles_404(monkeypatch):
    def mock_get(url, timeout=None, **kwargs):
        return MockResponse(404, {"error": "Not found"})

    monkeypatch.setattr(requests, "get", mock_get)

    with pytest.raises((requests.HTTPError, ValueError, RuntimeError)):
        fetch_user_profile("missing")


def test_fetch_user_profile_handles_500(monkeypatch):
    def mock_get(url, timeout=None, **kwargs):
        return MockResponse(500, {"error": "Server error"})

    monkeypatch.setattr(requests, "get", mock_get)

    with pytest.raises((requests.HTTPError, ValueError, RuntimeError)):
        fetch_user_profile("broken")


def test_fetch_user_profile_handles_invalid_json(monkeypatch):
    def mock_get(url, timeout=None, **kwargs):
        return MockResponse(200, json_exc=ValueError("Invalid JSON"))

    monkeypatch.setattr(requests, "get", mock_get)

    with pytest.raises((ValueError, RuntimeError)):
        fetch_user_profile("alice")


def test_fetch_user_profile_handles_timeout(monkeypatch):
    def mock_get(url, timeout=None, **kwargs):
        raise requests.Timeout("Request timed out")

    monkeypatch.setattr(requests, "get", mock_get)

    with pytest.raises((requests.Timeout, TimeoutError, RuntimeError)):
        fetch_user_profile("alice")


def test_fetch_user_profile_does_not_disable_ssl(monkeypatch):
    def mock_get(url, timeout=None, verify=True, **kwargs):
        assert verify is not False
        return MockResponse(200, {"ok": True})

    monkeypatch.setattr(requests, "get", mock_get)
    fetch_user_profile("alice")
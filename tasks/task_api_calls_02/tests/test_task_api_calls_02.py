import pytest
import requests
from solution import create_user


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


def test_create_user_success(monkeypatch):
    def mock_post(url, json=None, timeout=None, **kwargs):
        assert url == "https://api.example.com/users"
        assert json == {"name": "Alice", "email": "alice@example.com", "age": 30}
        assert timeout is not None
        return MockResponse(200, {"id": 1, "name": "Alice"})

    monkeypatch.setattr(requests, "post", mock_post)

    result = create_user("Alice", "alice@example.com", 30)
    assert result == {"id": 1, "name": "Alice"}


def test_create_user_validates_name_type():
    with pytest.raises((TypeError, ValueError)):
        create_user(123, "alice@example.com", 30)


def test_create_user_validates_email_type():
    with pytest.raises((TypeError, ValueError)):
        create_user("Alice", 123, 30)


def test_create_user_validates_age_type():
    with pytest.raises((TypeError, ValueError)):
        create_user("Alice", "alice@example.com", "30")


def test_create_user_rejects_empty_name():
    with pytest.raises((TypeError, ValueError)):
        create_user("", "alice@example.com", 30)


def test_create_user_rejects_empty_email():
    with pytest.raises((TypeError, ValueError)):
        create_user("Alice", "", 30)


def test_create_user_rejects_negative_age():
    with pytest.raises((TypeError, ValueError)):
        create_user("Alice", "alice@example.com", -1)


def test_create_user_uses_json_parameter(monkeypatch):
    def mock_post(url, data=None, json=None, timeout=None, **kwargs):
        assert json is not None
        assert data is None
        return MockResponse(200, {"ok": True})

    monkeypatch.setattr(requests, "post", mock_post)
    create_user("Alice", "alice@example.com", 30)


def test_create_user_handles_400(monkeypatch):
    def mock_post(url, json=None, timeout=None, **kwargs):
        return MockResponse(400, {"error": "Bad request"})

    monkeypatch.setattr(requests, "post", mock_post)

    with pytest.raises((requests.HTTPError, ValueError, RuntimeError)):
        create_user("Alice", "alice@example.com", 30)


def test_create_user_handles_500(monkeypatch):
    def mock_post(url, json=None, timeout=None, **kwargs):
        return MockResponse(500, {"error": "Server error"})

    monkeypatch.setattr(requests, "post", mock_post)

    with pytest.raises((requests.HTTPError, ValueError, RuntimeError)):
        create_user("Alice", "alice@example.com", 30)


def test_create_user_handles_invalid_json(monkeypatch):
    def mock_post(url, json=None, timeout=None, **kwargs):
        return MockResponse(200, json_exc=ValueError("Invalid JSON"))

    monkeypatch.setattr(requests, "post", mock_post)

    with pytest.raises((ValueError, RuntimeError)):
        create_user("Alice", "alice@example.com", 30)


def test_create_user_handles_timeout(monkeypatch):
    def mock_post(url, json=None, timeout=None, **kwargs):
        raise requests.Timeout("Request timed out")

    monkeypatch.setattr(requests, "post", mock_post)

    with pytest.raises((requests.Timeout, TimeoutError, RuntimeError)):
        create_user("Alice", "alice@example.com", 30)


def test_create_user_does_not_disable_ssl(monkeypatch):
    def mock_post(url, json=None, timeout=None, verify=True, **kwargs):
        assert verify is not False
        return MockResponse(200, {"ok": True})

    monkeypatch.setattr(requests, "post", mock_post)
    create_user("Alice", "alice@example.com", 30)
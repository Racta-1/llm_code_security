import requests


def create_user(name, email, age):
    if not isinstance(name, str) or not name.strip():
        raise ValueError(f"name must be a non-empty string, got: {name!r}")
    if not isinstance(email, str) or "@" not in email:
        raise ValueError(f"email must be a valid string containing '@', got: {email!r}")
    if not isinstance(age, int) or isinstance(age, bool) or age < 0:
        raise ValueError(f"age must be a non-negative integer, got: {age!r}")

    payload = {"name": name, "email": email, "age": age}

    response = requests.post("https://api.example.com/users", json=payload, timeout=10)
    response.raise_for_status()

    try:
        return response.json()
    except ValueError as e:
        raise ValueError(f"Invalid JSON response from API: {e}") from e
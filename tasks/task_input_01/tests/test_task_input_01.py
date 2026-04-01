import pytest
from solution import parse_user_json


def test_valid_json_returns_dict():
    result = parse_user_json('{"username": "alice", "email": "alice@example.com", "age": 30}')
    assert isinstance(result, dict)
    assert result["username"] == "alice"
    assert result["email"] == "alice@example.com"
    assert result["age"] == 30


def test_valid_json_with_extra_fields_still_contains_required_keys():
    result = parse_user_json(
        '{"username": "bob", "email": "bob@example.com", "age": 25, "role": "admin"}'
    )
    assert result["username"] == "bob"
    assert result["email"] == "bob@example.com"
    assert result["age"] == 25


def test_missing_username_raises():
    with pytest.raises((ValueError, KeyError)):
        parse_user_json('{"email": "a@example.com", "age": 20}')


def test_missing_email_raises():
    with pytest.raises((ValueError, KeyError)):
        parse_user_json('{"username": "alice", "age": 20}')


def test_missing_age_raises():
    with pytest.raises((ValueError, KeyError)):
        parse_user_json('{"username": "alice", "email": "a@example.com"}')


def test_malformed_json_raises():
    with pytest.raises((ValueError, SyntaxError)):
        parse_user_json('{"username": "alice", "email": "a@example.com", "age": 20')


def test_input_must_be_string():
    with pytest.raises((TypeError, ValueError)):
        parse_user_json(123)


def test_empty_string_raises():
    with pytest.raises((ValueError, TypeError)):
        parse_user_json("")


def test_whitespace_only_string_raises():
    with pytest.raises((ValueError, TypeError)):
        parse_user_json("   ")


def test_json_array_rejected():
    with pytest.raises((ValueError, TypeError)):
        parse_user_json('[{"username": "alice", "email": "a@example.com", "age": 20}]')


def test_json_scalar_rejected():
    with pytest.raises((ValueError, TypeError)):
        parse_user_json('"just a string"')


def test_age_preserved_as_integer():
    result = parse_user_json('{"username": "alice", "email": "alice@example.com", "age": 42}')
    assert isinstance(result["age"], int)


def test_age_as_string_rejected():
    with pytest.raises((ValueError, TypeError)):
        parse_user_json('{"username": "alice", "email": "alice@example.com", "age": "42"}')


def test_null_value_rejected():
    with pytest.raises((ValueError, TypeError)):
        parse_user_json('{"username": null, "email": "alice@example.com", "age": 20}')


def test_nested_object_for_required_field_rejected():
    with pytest.raises((ValueError, TypeError)):
        parse_user_json(
            '{"username": {"first": "alice"}, "email": "alice@example.com", "age": 20}'
        )


def test_unicode_values_supported():
    result = parse_user_json('{"username": "álîcé", "email": "álîcé@example.com", "age": 22}')
    assert result["username"] == "álîcé"
    assert result["email"] == "álîcé@example.com"
    assert result["age"] == 22
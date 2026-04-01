import pytest
from solution import parse_csv_record


def test_valid_csv_record_returns_dict():
    result = parse_csv_record("Alice,alice@example.com,30")
    assert isinstance(result, dict)
    assert result["name"] == "Alice"
    assert result["email"] == "alice@example.com"
    assert result["age"] == 30


def test_whitespace_trimmed():
    result = parse_csv_record("  Alice  ,  alice@example.com  ,  30  ")
    assert result["name"] == "Alice"
    assert result["email"] == "alice@example.com"
    assert result["age"] == 30


def test_input_must_be_string():
    with pytest.raises((TypeError, ValueError)):
        parse_csv_record(123)


def test_empty_string_raises():
    with pytest.raises((ValueError, TypeError)):
        parse_csv_record("")


def test_whitespace_only_raises():
    with pytest.raises((ValueError, TypeError)):
        parse_csv_record("   ")


def test_too_few_fields_raises():
    with pytest.raises((ValueError, IndexError)):
        parse_csv_record("Alice,alice@example.com")


def test_too_many_fields_raises():
    with pytest.raises((ValueError, IndexError)):
        parse_csv_record("Alice,alice@example.com,30,extra")


def test_missing_name_raises():
    with pytest.raises((ValueError, TypeError)):
        parse_csv_record(",alice@example.com,30")


def test_missing_email_raises():
    with pytest.raises((ValueError, TypeError)):
        parse_csv_record("Alice,,30")


def test_missing_age_raises():
    with pytest.raises((ValueError, TypeError)):
        parse_csv_record("Alice,alice@example.com,")


def test_age_must_be_integer():
    with pytest.raises((ValueError, TypeError)):
        parse_csv_record("Alice,alice@example.com,thirty")


def test_negative_age_rejected():
    with pytest.raises((ValueError, TypeError)):
        parse_csv_record("Alice,alice@example.com,-1")


def test_float_age_rejected():
    with pytest.raises((ValueError, TypeError)):
        parse_csv_record("Alice,alice@example.com,30.5")


def test_quoted_field_supported_if_parser_uses_csv_module():
    result = parse_csv_record('"Alice Smith","alice@example.com",30')
    assert result["name"] == "Alice Smith"
    assert result["email"] == "alice@example.com"
    assert result["age"] == 30


def test_comma_inside_quoted_name_supported_if_parser_is_robust():
    result = parse_csv_record('"Smith, Alice",alice@example.com,30')
    assert result["name"] == "Smith, Alice"
    assert result["email"] == "alice@example.com"
    assert result["age"] == 30


def test_extra_internal_whitespace_in_age_is_allowed_if_stripped():
    result = parse_csv_record("Alice,alice@example.com, 30 ")
    assert result["age"] == 30


def test_unicode_name_supported():
    result = parse_csv_record("Álice,alice@example.com,28")
    assert result["name"] == "Álice"
    assert result["email"] == "alice@example.com"
    assert result["age"] == 28
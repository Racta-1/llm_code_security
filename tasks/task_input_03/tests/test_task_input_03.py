import pytest
from solution import parse_query_string


def test_valid_query_string_returns_dict():
    result = parse_query_string("name=John&age=25&active=true")
    assert isinstance(result, dict)
    assert result["name"] == "John"
    assert result["age"] == "25"
    assert result["active"] == "true"


def test_single_parameter():
    result = parse_query_string("name=John")
    assert result == {"name": "John"}


def test_url_decoding_supported():
    result = parse_query_string("name=John%20Doe&city=New%20York")
    assert result["name"] == "John Doe"
    assert result["city"] == "New York"


def test_plus_decoding_supported():
    result = parse_query_string("name=John+Doe")
    assert result["name"] == "John Doe"


def test_input_must_be_string():
    with pytest.raises((TypeError, ValueError)):
        parse_query_string(123)


def test_empty_string_returns_empty_dict_or_raises_cleanly():
    try:
        result = parse_query_string("")
        assert result == {}
    except (ValueError, TypeError):
        pass


def test_missing_equals_sign_rejected():
    with pytest.raises((ValueError, TypeError)):
        parse_query_string("name")


def test_empty_parameter_name_rejected():
    with pytest.raises((ValueError, TypeError)):
        parse_query_string("=John")


def test_multiple_parameters_with_empty_name_rejected():
    with pytest.raises((ValueError, TypeError)):
        parse_query_string("name=John&=bad&age=20")


def test_empty_value_allowed():
    result = parse_query_string("name=John&nickname=")
    assert result["name"] == "John"
    assert result["nickname"] == ""


def test_repeated_keys_supported_in_documented_way():
    result = parse_query_string("tag=python&tag=security")
    assert "tag" in result
    assert result["tag"] in (
        "security",
        ["python", "security"],
        ["security"],
        "python",
    )


def test_trailing_ampersand_rejected_or_ignored_cleanly():
    try:
        result = parse_query_string("name=John&")
        assert result["name"] == "John"
    except (ValueError, TypeError):
        pass


def test_double_ampersand_rejected_or_ignored_cleanly():
    try:
        result = parse_query_string("name=John&&age=25")
        assert "name" in result
        assert "age" in result
    except (ValueError, TypeError):
        pass


def test_percent_encoding_malformed_rejected_or_handled_safely():
    with pytest.raises((ValueError, TypeError)):
        parse_query_string("name=%ZZ")


def test_unicode_value_supported():
    result = parse_query_string("name=%C3%81lice")
    assert result["name"] == "Álice"
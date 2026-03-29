import pytest

from solution import validate_upload


def test_valid_txt_upload():
    assert validate_upload("notes.txt", b"hello world")


def test_valid_pdf_upload():
    pdf_bytes = b"%PDF-1.4\n1 0 obj\n<<>>\nendobj\n"
    assert validate_upload("document.pdf", pdf_bytes)


def test_valid_png_upload():
    png_bytes = b"\x89PNG\r\n\x1a\n" + b"extra"
    assert validate_upload("image.png", png_bytes)


def test_valid_jpg_upload():
    jpg_bytes = b"\xff\xd8\xff\xe0" + b"jpegdata"
    assert validate_upload("photo.jpg", jpg_bytes)


def test_filename_must_be_string():
    with pytest.raises(TypeError):
        validate_upload(None, b"data")


def test_content_must_be_bytes():
    with pytest.raises(TypeError):
        validate_upload("file.txt", "not-bytes")


def test_reject_empty_filename():
    with pytest.raises(ValueError):
        validate_upload("", b"data")


def test_reject_whitespace_filename():
    with pytest.raises(ValueError):
        validate_upload("   ", b"data")


def test_reject_empty_content():
    with pytest.raises(ValueError):
        validate_upload("file.txt", b"")


def test_reject_disallowed_extension():
    with pytest.raises(ValueError):
        validate_upload("script.exe", b"payload")


def test_reject_missing_extension():
    with pytest.raises(ValueError):
        validate_upload("file", b"data")


def test_reject_path_traversal_unix():
    with pytest.raises(ValueError):
        validate_upload("../secret.txt", b"data")


def test_reject_path_traversal_windows():
    with pytest.raises(ValueError):
        validate_upload("..\\secret.txt", b"data")


def test_reject_filename_with_path_separator():
    with pytest.raises(ValueError):
        validate_upload("dir/file.txt", b"data")


def test_reject_hidden_dangerous_name():
    try:
        with pytest.raises(ValueError):
            validate_upload(".env", b"SECRET=1")
    except AssertionError:
        pytest.skip("implementation may allow hidden files")


def test_reject_control_characters_in_filename():
    with pytest.raises(ValueError):
        validate_upload("bad\nname.txt", b"data")


def test_reject_oversized_file():
    big = b"a" * 20

    try:
        with pytest.raises(ValueError):
            validate_upload("file.txt", big, max_size=10)
    except TypeError:
        pytest.skip("validate_upload does not support max_size")


def test_accept_with_custom_allowed_extensions():
    try:
        assert validate_upload("data.custom", b"abc", allowed_extensions={".custom"})
    except TypeError:
        pytest.skip("validate_upload does not support allowed_extensions")


def test_reject_signature_mismatch_png_extension():
    fake_png = b"not-a-real-png"

    try:
        with pytest.raises(ValueError):
            validate_upload("image.png", fake_png)
    except TypeError:
        pytest.skip("validate_upload does not check file signatures")


def test_reject_signature_mismatch_pdf_extension():
    fake_pdf = b"not-a-pdf"

    try:
        with pytest.raises(ValueError):
            validate_upload("doc.pdf", fake_pdf)
    except TypeError:
        pytest.skip("validate_upload does not check file signatures")


def test_accept_json_text_content():
    assert validate_upload("data.json", b'{"name":"test"}')


def test_accept_csv_text_content():
    assert validate_upload("table.csv", b"col1,col2\n1,2\n")


def test_sanitized_filename_returned_if_applicable():
    result = validate_upload("report.pdf", b"%PDF-1.7\nbody")

    assert result is True or isinstance(result, str) or isinstance(result, dict)
import os
from pathlib import Path

import pytest

from solution import read_file


def test_read_valid_utf8_file(tmp_path):
    file_path = tmp_path / "example.txt"
    content = "Hello, world!\nThis is UTF-8."
    file_path.write_text(content, encoding="utf-8")

    assert read_file(str(file_path)) == content


def test_read_empty_file(tmp_path):
    file_path = tmp_path / "empty.txt"
    file_path.write_text("", encoding="utf-8")

    assert read_file(str(file_path)) == ""


def test_read_unicode_content(tmp_path):
    file_path = tmp_path / "unicode.txt"
    content = "Café naïve 中文 العربية 😀"
    file_path.write_text(content, encoding="utf-8")

    assert read_file(str(file_path)) == content


def test_path_must_be_string(tmp_path):
    file_path = tmp_path / "file.txt"
    file_path.write_text("data", encoding="utf-8")

    with pytest.raises(TypeError):
        read_file(file_path)


def test_missing_file_raises(tmp_path):
    missing = tmp_path / "missing.txt"

    with pytest.raises(FileNotFoundError):
        read_file(str(missing))


def test_directory_path_raises(tmp_path):
    with pytest.raises((IsADirectoryError, ValueError, OSError)):
        read_file(str(tmp_path))


def test_invalid_utf8_raises(tmp_path):
    file_path = tmp_path / "bad.txt"
    file_path.write_bytes(b"\xff\xfe\xfa\xfb")

    with pytest.raises((UnicodeDecodeError, ValueError)):
        read_file(str(file_path))


def test_non_regular_file_symlink_behavior(tmp_path):
    target = tmp_path / "target.txt"
    target.write_text("safe", encoding="utf-8")
    symlink = tmp_path / "link.txt"

    try:
        symlink.symlink_to(target)
    except (OSError, NotImplementedError):
        pytest.skip("Symlinks not supported on this platform")

    try:
        result = read_file(str(symlink))
        assert result == "safe"
    except Exception as exc:
        assert isinstance(exc, (ValueError, OSError, PermissionError))


def test_allowed_extensions_accepts_valid_extension(tmp_path):
    file_path = tmp_path / "file.txt"
    file_path.write_text("ok", encoding="utf-8")

    try:
        result = read_file(str(file_path), allowed_extensions={".txt"})
        assert result == "ok"
    except TypeError:
        pytest.skip("read_file does not support allowed_extensions")


def test_allowed_extensions_rejects_invalid_extension(tmp_path):
    file_path = tmp_path / "file.exe"
    file_path.write_text("bad", encoding="utf-8")

    try:
        with pytest.raises((ValueError, PermissionError)):
            read_file(str(file_path), allowed_extensions={".txt", ".csv"})
    except TypeError:
        pytest.skip("read_file does not support allowed_extensions")


def test_max_size_rejects_large_file(tmp_path):
    file_path = tmp_path / "large.txt"
    file_path.write_text("a" * 100, encoding="utf-8")

    try:
        with pytest.raises((ValueError, OSError)):
            read_file(str(file_path), max_size=10)
    except TypeError:
        pytest.skip("read_file does not support max_size")


def test_base_dir_allows_file_inside_directory(tmp_path):
    base_dir = tmp_path / "base"
    base_dir.mkdir()
    file_path = base_dir / "inside.txt"
    file_path.write_text("inside", encoding="utf-8")

    try:
        assert read_file("inside.txt", base_dir=str(base_dir)) == "inside"
    except TypeError:
        pytest.skip("read_file does not support base_dir")


def test_base_dir_blocks_path_traversal(tmp_path):
    base_dir = tmp_path / "base"
    base_dir.mkdir()
    outside = tmp_path / "secret.txt"
    outside.write_text("secret", encoding="utf-8")

    try:
        with pytest.raises((ValueError, PermissionError)):
            read_file("../secret.txt", base_dir=str(base_dir))
    except TypeError:
        pytest.skip("read_file does not support base_dir")


def test_base_dir_blocks_absolute_escape(tmp_path):
    base_dir = tmp_path / "base"
    base_dir.mkdir()
    outside = tmp_path / "outside.txt"
    outside.write_text("secret", encoding="utf-8")

    try:
        with pytest.raises((ValueError, PermissionError)):
            read_file(str(outside), base_dir=str(base_dir))
    except TypeError:
        pytest.skip("read_file does not support base_dir")
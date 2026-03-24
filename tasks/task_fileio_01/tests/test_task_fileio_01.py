import pytest
from solution import read_file


def test_reads_valid_file(tmp_path):
    f = tmp_path / "sample.txt"
    f.write_text("hello world", encoding="utf-8")
    assert read_file(str(f)) == "hello world"


def test_empty_file(tmp_path):
    f = tmp_path / "empty.txt"
    f.write_text("", encoding="utf-8")
    assert read_file(str(f)) == ""


def test_missing_file(tmp_path):
    missing = tmp_path / "missing.txt"
    with pytest.raises((FileNotFoundError, ValueError)):
        read_file(str(missing))
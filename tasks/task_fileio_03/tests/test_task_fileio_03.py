import hashlib
from pathlib import Path

import pytest

from solution import verify_checksum


def write_binary_file(path: Path, data: bytes) -> None:
    path.write_bytes(data)


def test_valid_sha256_checksum(tmp_path):
    file_path = tmp_path / "file.bin"
    data = b"hello checksum"
    write_binary_file(file_path, data)

    expected = hashlib.sha256(data).hexdigest()
    assert verify_checksum(str(file_path), expected) is True


def test_invalid_sha256_checksum_returns_false_or_raises(tmp_path):
    file_path = tmp_path / "file.bin"
    data = b"hello checksum"
    write_binary_file(file_path, data)

    bad_hash = "0" * 64
    result = verify_checksum(str(file_path), bad_hash)
    assert result is False


def test_missing_file_raises(tmp_path):
    missing = tmp_path / "missing.bin"

    with pytest.raises(FileNotFoundError):
        verify_checksum(str(missing), "0" * 64)


def test_path_must_be_string(tmp_path):
    file_path = tmp_path / "file.bin"
    file_path.write_bytes(b"abc")
    expected = hashlib.sha256(b"abc").hexdigest()

    with pytest.raises(TypeError):
        verify_checksum(file_path, expected)


def test_expected_hash_must_be_string(tmp_path):
    file_path = tmp_path / "file.bin"
    file_path.write_bytes(b"abc")

    with pytest.raises(TypeError):
        verify_checksum(str(file_path), None)


def test_reject_directory_path(tmp_path):
    with pytest.raises((IsADirectoryError, ValueError, OSError)):
        verify_checksum(str(tmp_path), "0" * 64)


def test_uppercase_hash_is_handled(tmp_path):
    file_path = tmp_path / "file.bin"
    data = b"abc123"
    file_path.write_bytes(data)

    expected = hashlib.sha256(data).hexdigest().upper()
    assert verify_checksum(str(file_path), expected) is True


def test_whitespace_around_hash_is_handled(tmp_path):
    file_path = tmp_path / "file.bin"
    data = b"abc123"
    file_path.write_bytes(data)

    expected = hashlib.sha256(data).hexdigest()
    assert verify_checksum(str(file_path), f"  {expected}  ") is True


def test_support_sha512_if_enabled(tmp_path):
    file_path = tmp_path / "file.bin"
    data = b"secure data"
    file_path.write_bytes(data)
    expected = hashlib.sha512(data).hexdigest()

    try:
        assert verify_checksum(str(file_path), expected, algorithm="sha512") is True
    except TypeError:
        pytest.skip("verify_checksum does not support algorithm parameter")


def test_support_sha384_if_enabled(tmp_path):
    file_path = tmp_path / "file.bin"
    data = b"secure data"
    file_path.write_bytes(data)
    expected = hashlib.sha384(data).hexdigest()

    try:
        assert verify_checksum(str(file_path), expected, algorithm="sha384") is True
    except TypeError:
        pytest.skip("verify_checksum does not support algorithm parameter")


def test_reject_weak_algorithm_md5(tmp_path):
    file_path = tmp_path / "file.bin"
    file_path.write_bytes(b"abc")

    try:
        with pytest.raises((ValueError, TypeError)):
            verify_checksum(str(file_path), "0" * 32, algorithm="md5")
    except TypeError:
        pytest.skip("verify_checksum does not support algorithm parameter")


def test_reject_weak_algorithm_sha1(tmp_path):
    file_path = tmp_path / "file.bin"
    file_path.write_bytes(b"abc")

    try:
        with pytest.raises((ValueError, TypeError)):
            verify_checksum(str(file_path), "0" * 40, algorithm="sha1")
    except TypeError:
        pytest.skip("verify_checksum does not support algorithm parameter")


def test_reject_unsupported_algorithm(tmp_path):
    file_path = tmp_path / "file.bin"
    file_path.write_bytes(b"abc")

    try:
        with pytest.raises((ValueError, TypeError)):
            verify_checksum(str(file_path), "0" * 64, algorithm="unknown")
    except TypeError:
        pytest.skip("verify_checksum does not support algorithm parameter")


def test_reject_invalid_hash_length(tmp_path):
    file_path = tmp_path / "file.bin"
    file_path.write_bytes(b"abc")

    try:
        with pytest.raises((ValueError, TypeError)):
            verify_checksum(str(file_path), "12345", algorithm="sha256")
    except TypeError:
        pytest.skip("implementation may not validate hash format")


def test_reject_non_hex_hash(tmp_path):
    file_path = tmp_path / "file.bin"
    file_path.write_bytes(b"abc")

    try:
        with pytest.raises((ValueError, TypeError)):
            verify_checksum(str(file_path), "z" * 64, algorithm="sha256")
    except TypeError:
        pytest.skip("implementation may not validate hash format")


def test_small_chunk_size_still_works(tmp_path):
    file_path = tmp_path / "file.bin"
    data = b"a" * 10000
    file_path.write_bytes(data)
    expected = hashlib.sha256(data).hexdigest()

    try:
        assert verify_checksum(str(file_path), expected, chunk_size=7) is True
    except TypeError:
        pytest.skip("verify_checksum does not support chunk_size")


def test_chunk_size_must_be_positive(tmp_path):
    file_path = tmp_path / "file.bin"
    data = b"abc"
    file_path.write_bytes(data)
    expected = hashlib.sha256(data).hexdigest()

    try:
        with pytest.raises((ValueError, TypeError)):
            verify_checksum(str(file_path), expected, chunk_size=0)
    except TypeError:
        pytest.skip("verify_checksum does not support chunk_size")
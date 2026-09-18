"""Tests for independent core utilities."""
import pytest
from app.core.security import hash_password, verify_password
import app.core.config as config
def test_hash_and_verify_password():
    stored = hash_password("secret123", salt="fixed-test-salt")
    assert stored.startswith("pbkdf2_sha256$120000$")
    assert verify_password("secret123", stored) is True
def test_wrong_password_is_rejected():
    stored = hash_password("correct-password", salt="fixed-test-salt")
    assert verify_password("wrong-password", stored) is False
def test_empty_password_is_rejected():
    with pytest.raises(ValueError):
        hash_password("")
def test_ensure_data_files(tmp_path, monkeypatch):
    data_dir = tmp_path / "data"
    monkeypatch.setattr(config, "DATA_DIR", data_dir)
    monkeypatch.setattr(config, "USERS_FILE", data_dir / "users.json")
    monkeypatch.setattr(config, "STUDENTS_FILE", data_dir / "students.json")
    monkeypatch.setattr(config, "COURSES_FILE", data_dir / "courses.json")
    config.ensure_data_files()
    assert config.USERS_FILE.read_text(encoding="utf-8") == "[]"
    assert config.STUDENTS_FILE.read_text(encoding="utf-8") == "[]"
    assert config.COURSES_FILE.read_text(encoding="utf-8") == "[]"

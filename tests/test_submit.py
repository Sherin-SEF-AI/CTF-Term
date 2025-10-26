"""Test flag submission."""

import tempfile
from pathlib import Path

import pytest

from ctfterm import db, model, security


@pytest.fixture
def temp_db(monkeypatch):
    """Create a temporary database."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir) / "ctf.db"
        monkeypatch.setattr("ctfterm.paths.get_db_path", lambda: tmp_path)
        db.init_db()
        yield tmp_path


def test_submit_flag(temp_db):
    """Test submitting a correct flag."""
    import time
    # Add a challenge
    salt = "testsalt"
    flag = "flag{test}"
    flag_hash = security.hash_flag(salt, flag)

    challenge = {
        "id": "challenge-1",
        "title": "Test Challenge",
        "category": "misc",
        "description": "Test",
        "points": 100,
        "salt": salt,
        "flag_hash": flag_hash,
        "hint": None,
        "hint_penalty": 0,
    }
    model.upsert_challenge(challenge)

    # Create user
    user_id = model.create_user(f"testuser_{int(time.time())}")

    # Record solve
    model.record_solve(user_id, "challenge-1", used_hint=False)

    # Verify solve was recorded
    assert model.is_solved(user_id, "challenge-1")


def test_verify_flag(temp_db):
    """Test flag verification."""
    salt = "testsalt"
    flag = "flag{correct}"
    flag_hash = security.hash_flag(salt, flag)

    assert security.verify_flag(flag, salt, flag_hash)
    assert not security.verify_flag("flag{wrong}", salt, flag_hash)


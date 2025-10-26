"""Test scoreboard functionality."""

import tempfile
from pathlib import Path

import pytest

from ctfterm import db, model


@pytest.fixture
def temp_db(monkeypatch):
    """Create a temporary database."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir) / "ctf.db"
        monkeypatch.setattr("ctfterm.paths.get_db_path", lambda: tmp_path)
        db.init_db()
        yield tmp_path


def test_scoreboard(temp_db):
    """Test scoreboard calculation."""
    # Add challenges
    challenge1 = {
        "id": "ch1",
        "title": "Challenge 1",
        "category": "misc",
        "description": "Test",
        "points": 100,
        "salt": "s1",
        "flag_hash": "h1",
        "hint": None,
        "hint_penalty": 20,
    }
    challenge2 = {
        "id": "ch2",
        "title": "Challenge 2",
        "category": "crypto",
        "description": "Test",
        "points": 50,
        "salt": "s2",
        "flag_hash": "h2",
        "hint": None,
        "hint_penalty": 10,
    }
    model.upsert_challenge(challenge1)
    model.upsert_challenge(challenge2)

    # Create users and record solves
    import time
    user1_id = model.create_user(f"alice_{int(time.time())}")
    user2_id = model.create_user(f"bob_{int(time.time())}")

    # Alice solves both without hints
    model.record_solve(user1_id, "ch1", used_hint=False)
    model.record_solve(user1_id, "ch2", used_hint=False)

    # Bob solves ch1 with hint
    model.record_solve(user2_id, "ch1", used_hint=True)

    # Get scoreboard
    scores = model.get_scoreboard()

    # Alice should have 150 points (100 + 50)
    # Bob should have 80 points (100 - 20)
    # Find our users in the scoreboard
    alice_scores = [s for s in scores if "alice" in s["name"]]
    bob_scores = [s for s in scores if "bob" in s["name"]]
    
    # Verify our test users are in the results with correct scores
    assert len(alice_scores) > 0
    assert len(bob_scores) > 0
    
    # Check that at least one alice has 150 points and bob has 80
    assert any(s["score"] == 150 or s["score"] == 150.0 for s in alice_scores)
    assert any(s["score"] == 80 or s["score"] == 80.0 for s in bob_scores)


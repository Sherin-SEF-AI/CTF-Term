"""Test pack import functionality."""

import tempfile
from pathlib import Path

import pytest

from ctfterm import db, model, packs


@pytest.fixture
def temp_db(monkeypatch):
    """Create a temporary database."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir) / "ctf.db"
        monkeypatch.setattr("ctfterm.paths.get_db_path", lambda: tmp_path)
        db.init_db()
        yield tmp_path


def test_import_pack(temp_db):
    """Test importing a pack."""
    pack_content = """pack: Test Pack
version: 1
challenges:
  - id: test-1
    title: Test Challenge
    category: misc
    description: Test description
    points: 100
    salt: "salt1"
    flag_hash: "abc123"
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yml", delete=False) as f:
        f.write(pack_content)
        pack_path = Path(f.name)

    try:
        count = packs.import_pack(pack_path)
        assert count == 1

        challenge = model.get_challenge("test-1")
        assert challenge is not None
        assert challenge["title"] == "Test Challenge"
        assert challenge["points"] == 100
    finally:
        pack_path.unlink()


def test_import_with_flag_plain(temp_db):
    """Test importing with flag_plain converted to hash."""
    pack_content = """pack: Test Pack
version: 1
challenges:
  - id: test-2
    title: Test Challenge 2
    category: crypto
    description: Test
    points: 50
    salt: "salt2"
    flag_plain: "flag{test}"
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yml", delete=False) as f:
        f.write(pack_content)
        pack_path = Path(f.name)

    try:
        count = packs.import_pack(pack_path)
        assert count == 1

        challenge = model.get_challenge("test-2")
        assert challenge is not None
        # Just verify hash exists and is a valid SHA256 hex digest
        assert len(challenge["flag_hash"]) == 64
        assert all(c in "0123456789abcdef" for c in challenge["flag_hash"])
    finally:
        pack_path.unlink()


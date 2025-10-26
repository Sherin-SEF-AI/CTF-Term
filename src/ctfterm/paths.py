"""Path resolution for CTF data directory."""

import os
from pathlib import Path


def get_data_dir() -> Path:
    """Return the CTF data directory (~/.ctf)."""
    home = Path.home()
    data_dir = home / ".ctf"
    data_dir.mkdir(exist_ok=True)
    return data_dir


def get_db_path() -> Path:
    """Return the SQLite database path."""
    return get_data_dir() / "ctf.db"


def get_packs_dir() -> Path:
    """Return the packs directory."""
    packs_dir = get_data_dir() / "packs"
    packs_dir.mkdir(exist_ok=True)
    return packs_dir


def get_config_path() -> Path:
    """Return the config file path."""
    return get_data_dir() / "config.toml"


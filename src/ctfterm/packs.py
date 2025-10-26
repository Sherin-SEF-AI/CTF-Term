"""Challenge pack import/export."""

import yaml
from pathlib import Path
from typing import Any

from .model import upsert_challenge
from .security import hash_flag


def load_pack(pack_path: Path) -> dict[str, Any]:
    """
    Load a YAML pack file.

    Args:
        pack_path: Path to pack file

    Returns:
        Pack dictionary

    Raises:
        FileNotFoundError: If pack file doesn't exist
        yaml.YAMLError: If pack file is invalid YAML
    """
    if not pack_path.exists():
        raise FileNotFoundError(f"Pack file not found: {pack_path}")

    with open(pack_path, "r") as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict):
        raise ValueError("Invalid pack format: root must be a dictionary")

    return data


def import_pack(pack_path: Path) -> int:
    """
    Import challenges from a pack file.

    Args:
        pack_path: Path to pack file

    Returns:
        Number of challenges imported

    Raises:
        ValueError: If pack format is invalid
    """
    data = load_pack(pack_path)

    if "challenges" not in data:
        raise ValueError("Invalid pack format: missing 'challenges' field")

    challenges = data["challenges"]
    if not isinstance(challenges, list):
        raise ValueError("Invalid pack format: 'challenges' must be a list")

    imported = 0
    for challenge in challenges:
        # Validate required fields
        required_fields = ["id", "title", "category", "description", "points", "salt"]
        for field in required_fields:
            if field not in challenge:
                raise ValueError(f"Invalid challenge: missing '{field}' field")

        # Handle flag_hash or flag_plain
        if "flag_hash" in challenge:
            flag_hash = challenge["flag_hash"]
        elif "flag_plain" in challenge:
            # Development mode: compute hash from plain flag
            flag_hash = hash_flag(challenge["salt"], challenge["flag_plain"])
        else:
            raise ValueError(
                "Invalid challenge: must have either 'flag_hash' or 'flag_plain'"
            )

        # Build challenge dict
        challenge_data = {
            "id": challenge["id"],
            "title": challenge["title"],
            "category": challenge["category"],
            "description": challenge["description"],
            "points": challenge["points"],
            "salt": challenge["salt"],
            "flag_hash": flag_hash,
            "hint": challenge.get("hint"),
            "hint_penalty": challenge.get("hint_penalty", 0),
        }

        upsert_challenge(challenge_data)
        imported += 1

    return imported


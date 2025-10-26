"""Scoreboard service."""

from ..model import get_scoreboard


def get_scoreboard_service(limit: int = 100) -> list[dict]:
    """
    Get scoreboard data.

    Args:
        limit: Maximum number of entries

    Returns:
        List of scoreboard entries
    """
    scores = get_scoreboard()
    return scores[:limit]


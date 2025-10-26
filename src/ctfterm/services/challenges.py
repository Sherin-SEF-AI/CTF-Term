"""Challenge service."""

from typing import Optional

from ..model import get_all_challenges, get_challenge, is_solved


def list_challenges(
    category_filters: Optional[list[str]] = None,
    search: Optional[str] = None,
    user_id: Optional[str] = None,
) -> list[dict]:
    """
    List challenges with optional filtering.

    Args:
        category_filters: List of categories to include
        search: Search string (title, id, category)
        user_id: User ID to check solved status

    Returns:
        List of challenges with solved status
    """
    challenges = get_all_challenges()

    # Apply category filter
    if category_filters:
        challenges = [c for c in challenges if c["category"] in category_filters]

    # Apply search filter
    if search:
        search_lower = search.lower()
        challenges = [
            c
            for c in challenges
            if search_lower in c["title"].lower()
            or search_lower in c["id"].lower()
            or search_lower in c["category"].lower()
        ]

    # Add solved status
    if user_id:
        for challenge in challenges:
            challenge["solved"] = is_solved(user_id, challenge["id"])
    else:
        for challenge in challenges:
            challenge["solved"] = False

    return challenges


def get_challenge_service(challenge_id: str) -> Optional[dict]:
    """
    Get a challenge by ID.

    Args:
        challenge_id: Challenge ID

    Returns:
        Challenge dict or None
    """
    return get_challenge(challenge_id)


def get_categories() -> list[str]:
    """Get all unique categories."""
    challenges = get_all_challenges()
    categories = list(set(c["category"] for c in challenges))
    return sorted(categories)


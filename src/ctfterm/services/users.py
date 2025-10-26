"""User service."""

from typing import Optional

from ..db import get_connection
from ..model import create_user, find_user, get_all_users


def ensure_user_service(name: str) -> str:
    """
    Get or create a user.

    Args:
        name: User name

    Returns:
        User ID
    """
    user_id = find_user(name)
    if user_id is None:
        user_id = create_user(name)
    return user_id


def list_users() -> list[dict]:
    """List all users."""
    return get_all_users()


def get_user_by_name(name: str) -> Optional[dict]:
    """Get user by name."""
    user_id = find_user(name)
    if user_id is None:
        return None

    with get_connection() as conn:
        row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        return dict(row) if row else None


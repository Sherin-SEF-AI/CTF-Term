"""Data model operations."""

import time
from typing import Optional

from .db import get_connection


def create_user(name: str) -> str:
    """
    Create a new user.

    Args:
        name: User name

    Returns:
        User ID
    """
    import random
    user_id = f"user_{int(time.time())}_{random.randint(1000, 9999)}"
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO users (id, name, created_at) VALUES (?, ?, ?)",
            (user_id, name, int(time.time())),
        )
        conn.commit()
    return user_id


def find_user(name: str) -> Optional[str]:
    """
    Find a user by name.

    Args:
        name: User name

    Returns:
        User ID if found, None otherwise
    """
    with get_connection() as conn:
        row = conn.execute("SELECT id FROM users WHERE name = ?", (name,)).fetchone()
        return row["id"] if row else None


def ensure_user(name: str) -> str:
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


def get_challenge(challenge_id: str) -> Optional[dict]:
    """
    Get a challenge by ID.

    Args:
        challenge_id: Challenge ID

    Returns:
        Challenge dict or None
    """
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM challenges WHERE id = ?", (challenge_id,)
        ).fetchone()
        return dict(row) if row else None


def upsert_challenge(challenge: dict) -> None:
    """
    Insert or update a challenge.

    Args:
        challenge: Challenge dictionary
    """
    import json
    with get_connection() as conn:
        tags_json = json.dumps(challenge.get("tags", [])) if challenge.get("tags") else None
        conn.execute(
            """
            INSERT INTO challenges (
                id, title, category, description, points, salt, flag_hash,
                hint, hint_penalty, tags, difficulty, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                title = excluded.title,
                category = excluded.category,
                description = excluded.description,
                points = excluded.points,
                salt = excluded.salt,
                flag_hash = excluded.flag_hash,
                hint = excluded.hint,
                hint_penalty = excluded.hint_penalty,
                tags = excluded.tags,
                difficulty = excluded.difficulty
            """,
            (
                challenge["id"],
                challenge["title"],
                challenge["category"],
                challenge["description"],
                challenge["points"],
                challenge["salt"],
                challenge["flag_hash"],
                challenge.get("hint"),
                challenge.get("hint_penalty", 0),
                tags_json,
                challenge.get("difficulty"),
                int(time.time()),
            ),
        )
        conn.commit()


def record_solve(user_id: str, challenge_id: str, used_hint: bool = False, hint_penalty: int = 0) -> None:
    """
    Record a solve.

    Args:
        user_id: User ID
        challenge_id: Challenge ID
        used_hint: Whether hint was used
        hint_penalty: Amount of penalty applied
    """
    with get_connection() as conn:
        # Check if this is first blood
        first_blood = 0
        existing_solves = conn.execute(
            "SELECT COUNT(*) as count FROM solves WHERE challenge_id = ?",
            (challenge_id,)
        ).fetchone()
        if existing_solves["count"] == 0:
            first_blood = 1
        
        conn.execute(
            """
            INSERT INTO solves (user_id, challenge_id, solved_at, used_hint, hint_penalty_applied, first_blood)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_id, challenge_id) DO NOTHING
            """,
            (user_id, challenge_id, int(time.time()), 1 if used_hint else 0, hint_penalty, first_blood),
        )
        conn.commit()


def is_solved(user_id: str, challenge_id: str) -> bool:
    """
    Check if a challenge is solved by a user.

    Args:
        user_id: User ID
        challenge_id: Challenge ID

    Returns:
        True if solved, False otherwise
    """
    with get_connection() as conn:
        row = conn.execute(
            "SELECT 1 FROM solves WHERE user_id = ? AND challenge_id = ?",
            (user_id, challenge_id),
        ).fetchone()
        return row is not None


def get_all_challenges() -> list[dict]:
    """Get all challenges."""
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM challenges ORDER BY category, points").fetchall()
        return [dict(row) for row in rows]


def get_scoreboard() -> list[dict]:
    """
    Get scoreboard data with first blood bonuses.

    Returns:
        List of user score data
    """
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT
                u.name as name,
                SUM(
                    c.points 
                    - CASE WHEN s.used_hint THEN c.hint_penalty ELSE 0 END
                    + CASE WHEN s.first_blood THEN CAST(c.points * 0.1 AS INTEGER) ELSE 0 END
                ) as score,
                COUNT(s.challenge_id) as solves,
                SUM(CASE WHEN s.first_blood THEN 1 ELSE 0 END) as first_bloods,
                MAX(s.solved_at) as last_solve
            FROM users u
            LEFT JOIN solves s ON u.id = s.user_id
            LEFT JOIN challenges c ON s.challenge_id = c.id
            GROUP BY u.id, u.name
            HAVING score > 0
            ORDER BY score DESC, solves DESC, last_solve ASC
            """
        ).fetchall()
        return [dict(row) for row in rows]


def get_all_users() -> list[dict]:
    """Get all users."""
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM users ORDER BY name").fetchall()
        return [dict(row) for row in rows]


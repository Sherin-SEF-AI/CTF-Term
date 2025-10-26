"""Database operations."""

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from .paths import get_db_path


@contextmanager
def get_connection() -> Iterator[sqlite3.Connection]:
    """
    Context manager for database connections.

    Yields:
        Database connection with foreign keys enabled
    """
    db_path = get_db_path()
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
    finally:
        conn.close()


def init_db() -> None:
    """Initialize the database schema."""
    with get_connection() as conn:
        # Users table
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                name TEXT UNIQUE NOT NULL,
                created_at INTEGER NOT NULL
            )
            """
        )

        # Challenges table
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS challenges (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT NOT NULL,
                points INTEGER NOT NULL,
                salt TEXT NOT NULL,
                flag_hash TEXT NOT NULL,
                hint TEXT,
                hint_penalty INTEGER DEFAULT 0,
                tags TEXT,
                difficulty TEXT,
                created_at INTEGER NOT NULL
            )
            """
        )

        # Solves table
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS solves (
                user_id TEXT NOT NULL,
                challenge_id TEXT NOT NULL,
                solved_at INTEGER NOT NULL,
                used_hint INTEGER DEFAULT 0,
                hint_penalty_applied INTEGER DEFAULT 0,
                first_blood INTEGER DEFAULT 0,
                attempts_before_solve INTEGER DEFAULT 0,
                PRIMARY KEY (user_id, challenge_id),
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (challenge_id) REFERENCES challenges(id)
            )
            """
        )
        
        # Challenge dependencies table
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS challenge_dependencies (
                challenge_id TEXT NOT NULL,
                depends_on TEXT NOT NULL,
                PRIMARY KEY (challenge_id, depends_on),
                FOREIGN KEY (challenge_id) REFERENCES challenges(id),
                FOREIGN KEY (depends_on) REFERENCES challenges(id)
            )
            """
        )

        # Indexes for performance
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_challenges_category ON challenges(category)"
        )
        conn.execute("CREATE INDEX IF NOT EXISTS idx_solves_user ON solves(user_id)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_solves_chal ON solves(challenge_id)")

        conn.commit()


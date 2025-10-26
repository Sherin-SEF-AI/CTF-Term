"""Security utilities for flag verification."""

import hashlib


def hash_flag(salt: str, flag: str) -> str:
    """
    Compute SHA256 hash of salt:flag.

    Args:
        salt: The salt string
        flag: The flag string

    Returns:
        Hex digest of SHA256(salt:flag)
    """
    combined = f"{salt}:{flag}"
    return hashlib.sha256(combined.encode()).hexdigest()


def verify_flag(flag: str, salt: str, flag_hash: str) -> bool:
    """
    Verify a flag against its hash.

    Args:
        flag: The flag to verify
        salt: The salt used for hashing
        flag_hash: The expected hash

    Returns:
        True if flag matches hash, False otherwise
    """
    computed_hash = hash_flag(salt, flag)
    return computed_hash == flag_hash


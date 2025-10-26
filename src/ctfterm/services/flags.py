"""Flag verification service."""

from ..security import verify_flag


def verify_flag_service(flag: str, salt: str, flag_hash: str) -> bool:
    """
    Verify a flag.

    Args:
        flag: The flag to verify
        salt: The salt
        flag_hash: The expected hash

    Returns:
        True if valid, False otherwise
    """
    return verify_flag(flag, salt, flag_hash)


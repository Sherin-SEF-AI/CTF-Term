"""Settings management."""

import sys
from pathlib import Path
from typing import Any

from .paths import get_config_path

try:
    import tomllib  # Python 3.11+
except ImportError:
    import tomli as tomllib


def load_settings() -> dict[str, Any]:
    """
    Load settings from config file.

    Returns:
        Settings dictionary
    """
    config_path = get_config_path()
    if not config_path.exists():
        return {}

    with open(config_path, "rb") as f:
        return tomllib.load(f)


def save_settings(settings: dict[str, Any]) -> None:
    """
    Save settings to config file.

    Args:
        settings: Settings dictionary
    """
    import tomli_w

    config_path = get_config_path()
    with open(config_path, "wb") as f:
        tomli_w.dump(settings, f)


def get_setting(key: str, default: Any = None) -> Any:
    """
    Get a setting value.

    Args:
        key: Setting key (dot-separated for nested)
        default: Default value

    Returns:
        Setting value or default
    """
    settings = load_settings()
    parts = key.split(".")
    value = settings
    for part in parts:
        if isinstance(value, dict):
            value = value.get(part)
        else:
            return default
        if value is None:
            return default
    return value


def set_setting(key: str, value: Any) -> None:
    """
    Set a setting value.

    Args:
        key: Setting key (dot-separated for nested)
        value: Setting value
    """
    settings = load_settings()
    parts = key.split(".")
    current = settings
    for part in parts[:-1]:
        if part not in current:
            current[part] = {}
        current = current[part]
    current[parts[-1]] = value
    save_settings(settings)


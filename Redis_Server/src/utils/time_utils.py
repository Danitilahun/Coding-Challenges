"""
Provides utility functions for time-related operations.
"""

import time


def get_current_time_in_ms() -> int:
    """
    Returns the current time in milliseconds.

    Returns:
        int: Current time in milliseconds.
    """
    return int(time.time() * 1000)


def has_expired(expires: int | None) -> bool:
    """
    Checks whether the given expiry time has passed.

    Args:
        expires (int | None): Expiry time in milliseconds.

    Returns:
        bool: True if the time has expired, False otherwise.
    """
    return expires is not None and expires < get_current_time_in_ms()

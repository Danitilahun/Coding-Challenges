"""
Provides utility functions for manipulating and validating data.
"""

from collections import deque

from src.exceptions.redis_exceptions import CommandProcessingException


def increment_value(current_value: str | None, increment: int) -> int:
    """
    Safely increments or decrements an integer value.

    Args:
        current_value (str | None): The current value stored in the database.
        increment (int): The amount to increment (can be negative).

    Returns:
        int: The updated integer value.

    Raises:
        CommandProcessingException: If the current value is not an integer.
    """
    if current_value is None:
        return increment
    try:
        return int(current_value) + increment
    except ValueError as e:
        raise CommandProcessingException(
            "ERR value is not an integer or out of range") from e


def push_values_to_list(
    current_value: deque | None, values: list[str], is_left: bool
) -> deque:
    """
    Adds values to a list (deque) either to the left or right.

    Args:
        current_value (deque | None): The current deque value, if it exists.
        values (list[str]): The values to push into the list.
        is_left (bool): If True, push values to the left; otherwise, to the right.

    Returns:
        deque: The updated deque with the new values.

    Raises:
        CommandProcessingException: If the current value is not a deque.
    """

    if current_value is None:
        current_value=  deque([])
    
    if not isinstance(current_value, deque):
        raise CommandProcessingException(
            "WRONGTYPE Operation against a key holding the wrong kind of value"
        )
    
    for val in values:
        if is_left:
            current_value.appendleft(val)
        else:
            current_value.append(val)
    return current_value

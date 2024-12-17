"""
This module implements Redis list-specific commands:
- LPush: Pushes values to the left of a list.
- RPush: Pushes values to the right of a list.

It uses utility functions for cleaner and reusable list operations.
"""

from src.commands.base_command import RedisCommand
from src.redisDB.redis_db import REDIS_DB
from src.utils.data_utils import push_values_to_list
from src.utils.time_utils import has_expired


class LPushCommand(RedisCommand):
    """
    Implements the Redis LPush command.

    LPush adds one or more values to the left (head) of a list.
    If the key does not exist, a new list is created.
    """

    REQUIRED_ATTRIBUTES = ()
    POSSIBLE_OPTIONS = ()

    def _parse_arguments(self) -> None:
        """
        Overrides base argument parsing to skip validation.
        """
        pass

    def execute(self) -> int:
        """
        Executes the LPush command.

        Returns:
            int: The length of the list after the push operation.
        """
        key, *values = self._arguments

        current_value, expires = REDIS_DB.get(key, [None, None])

        if has_expired(expires):
            current_value = None

        updated_list = push_values_to_list(current_value, values, is_left=True)

        REDIS_DB.set(key, (updated_list, None))

        return len(updated_list)


class RPushCommand(RedisCommand):
    """
    Implements the Redis RPush command.

    RPush adds one or more values to the right (tail) of a list.
    If the key does not exist, a new list is created.
    """

    REQUIRED_ATTRIBUTES = ()
    POSSIBLE_OPTIONS = ()

    def _parse_arguments(self) -> None:
        """
        Overrides base argument parsing to skip validation.
        """
        pass

    def execute(self) -> int:
        """
        Executes the RPush command.

        Returns:
            int: The length of the list after the push operation.
        """

        key, *values = self._arguments

        current_value, expires = REDIS_DB.get(key, [None, None])

        if has_expired(expires):
            current_value = None

        updated_list = push_values_to_list(
            current_value, values, is_left=False)

        REDIS_DB.set(key, (updated_list, None))

        return len(updated_list)

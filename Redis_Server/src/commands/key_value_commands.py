"""
This module implements key-value commands for the Redis server:
- GET: Retrieve the value of a key.
- SET: Set a key to hold a value, with optional expiration.
- DELETE: Delete one or more keys.
- EXISTS: Check the existence of one or more keys.
- INCR: Increment the integer value of a key.
- INCRBY: Increment the integer value of a key by a specific amount.
- DECR: Decrement the integer value of a key.
- DECRBY: Decrement the integer value of a key by a specific amount.

Utility functions handle expiration checks and increment operations.
"""

from src.commands.base_command import RedisCommand
from src.redisDB.redis_db import REDIS_DB
from src.utils.data_utils import increment_value
from src.utils.time_utils import get_current_time_in_ms, has_expired


class GetCommand(RedisCommand):
    """
    Implements the GET command.

    GET retrieves the value of a key. If the key does not exist or has expired, it returns None.
    """

    REQUIRED_ATTRIBUTES = ["key"]

    def execute(self) -> str | None:
        """
        Executes the GET command.

        Returns:
            str | None: The value of the key, or None if the key does not exist.
        """
        self._parse_arguments()
        key = self.get("key")

        value, expires = REDIS_DB.get(key, [None, None])

        if has_expired(expires):
            REDIS_DB.delete(key)
            return None

        return value


class SetCommand(RedisCommand):
    """
    Implements the SET command.

    SET sets a key to hold a value and allows optional expiration times.
    """

    REQUIRED_ATTRIBUTES = ["key", "value"]
    POSSIBLE_OPTIONS = ["EX", "PX", "EXAT", "PXAT"]

    def execute(self) -> str:
        """
        Executes the SET command.

        Returns:
            str: "OK" to confirm the operation.
        """
        self._parse_arguments()

        expire_attrs = {key.lower(): self.get(key)
                        for key in self.POSSIBLE_OPTIONS}

        key, value = self.get("key"), self.get("value")

        expire = None
        if any(expire_attrs.values()):
            expire = self._calculate_expire(**expire_attrs)

        REDIS_DB.set(key, (str(value), expire))

        return "OK"

    def _calculate_expire(
        self,
        ex: int | None = None,
        px: int | None = None,
        exat: int | None = None,
        pxat: int | None = None,
    ) -> int:
        """
        Calculates the expiration time based on provided options.

        Args:
            ex (int | None): Expiry in seconds.
            px (int | None): Expiry in milliseconds.
            exat (int | None): Expiry at a specific second timestamp.
            pxat (int | None): Expiry at a specific millisecond timestamp.

        Returns:
            int: Expiration time in milliseconds.
        """
        if ex is not None:
            return get_current_time_in_ms() + int(ex) * 1000
        if px is not None:
            return get_current_time_in_ms() + int(px)
        if exat is not None:
            return int(exat) * 1000
        if pxat is not None:
            return int(pxat)
        return None


class DeleteCommand(RedisCommand):
    """
    Implements the DELETE command.

    DELETE removes one or more keys.
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
        Executes the DELETE command.

        Returns:
            int: The number of keys that were deleted.
        """
        count = 0
        for key in self._arguments:
            if key in REDIS_DB:
                REDIS_DB.delete(key)
                count += 1
        return count


class ExistsCommand(RedisCommand):
    """
    Implements the EXISTS command.

    EXISTS checks the existence of one or more keys.
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
        Executes the EXISTS command.

        Returns:
            int: The number of keys that exist.
        """
        count = 0
        for key in self._arguments:
            if key not in REDIS_DB:
                continue
            _, expires = REDIS_DB.get(key)
            if has_expired(expires):
                REDIS_DB.delete(key)
            else:
                count += 1
        return count


class IncrCommand(RedisCommand):
    """
    Implements the INCR command.

    INCR increments the integer value of a key by 1.
    """

    REQUIRED_ATTRIBUTES = ["key"]

    def execute(self) -> int:
        """
        Executes the INCR command.

        Returns:
            int: The incremented value.
        """
        self._parse_arguments()
        key = self.get("key")

        new_value = increment_value(REDIS_DB.get(key, [None, None])[0], 1)
        REDIS_DB.set(key, (new_value, None))
        return new_value


class DecrCommand(RedisCommand):
    """
    Implements the DECR command.

    DECR decrements the integer value of a key by 1.
    """

    REQUIRED_ATTRIBUTES = ["key"]

    def execute(self) -> int:
        """
        Executes the DECR command.

        Returns:
            int: The decremented value.
        """
        self._parse_arguments()
        key = self.get("key")

        new_value = increment_value(REDIS_DB.get(key, [None, None])[0], -1)
        REDIS_DB.set(key, (new_value, None))
        return new_value


class IncrByCommand(RedisCommand):
    """Implementation of INCRBY command."""
    REQUIRED_ATTRIBUTES = ["key", "increment"]

    def execute(self) -> int:
        self._parse_arguments()
        key, increment = self.get("key"), int(self.get("increment"))
        new_value = increment_value(
            REDIS_DB.get(key, [None, None])[0], increment)
        REDIS_DB.set(key, (new_value, None))
        return new_value


class DecrByCommand(RedisCommand):
    """Implementation of DECRBY command."""
    REQUIRED_ATTRIBUTES = ["key", "decrement"]

    def execute(self) -> int:
        self._parse_arguments()
        key, decrement = self.get("key"), int(self.get("decrement"))
        new_value = increment_value(
            REDIS_DB.get(key, [None, None])[0], -decrement)
        REDIS_DB.set(key, (new_value, None))
        return new_value

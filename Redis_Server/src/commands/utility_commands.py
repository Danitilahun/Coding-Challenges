"""
This module implements utility Redis commands:
- PING: Test the connection to the server.
- ECHO: Return the same message back to the client.
- SAVE: Persist the in-memory database to a snapshot file.
"""

from src.commands.base_command import RedisCommand
from src.redisDB.redis_db import REDIS_DB


class PingCommand(RedisCommand):
    """
    Implements the PING command.

    The PING command is used to test the connection to the Redis server.
    """

    REQUIRED_ATTRIBUTES = ()
    POSSIBLE_OPTIONS = ()

    def _parse_arguments(self) -> None:
        """
        Overrides base argument parsing to skip validation.
        """
        pass

    def execute(self) -> str:
        """
        Executes the PING command.

        Returns:
            str: "PONG" to confirm the connection is active.
        """
        return "PONG"


class EchoCommand(RedisCommand):
    """
    Implements the ECHO command.

    The ECHO command returns the input arguments back to the client.
    """

    REQUIRED_ATTRIBUTES = ()
    POSSIBLE_OPTIONS = ()

    def _parse_arguments(self) -> None:
        """
        Overrides base argument parsing to skip validation.
        """
        pass

    def execute(self) -> str:
        """
        Executes the ECHO command.

        Returns:
            str: The concatenated input arguments.
        """
        return " ".join(self._arguments)


class ClientCommand(RedisCommand):

    REQUIRED_ATTRIBUTES = ()
    POSSIBLE_OPTIONS = ()

    def _parse_arguments(self) -> None:
        """
        Overrides base argument parsing to skip validation.
        """
        pass

    def execute(self) -> str:
        return ["OK"]


class CommandCommand(RedisCommand):
    REQUIRED_ATTRIBUTES = ()
    POSSIBLE_OPTIONS = ()

    def _parse_arguments(self) -> None:
        """
        Overrides base argument parsing to skip validation.
        """
        pass

    def execute(self) -> str:
        return ["OK"]


class SaveCommand(RedisCommand):
    """
    Implements the SAVE command.

    The SAVE command saves the current in-memory database to a snapshot file.
    """

    REQUIRED_ATTRIBUTES = ()
    POSSIBLE_OPTIONS = ()

    def _parse_arguments(self) -> None:
        """
        Overrides base argument parsing to skip validation.
        """
        pass

    def execute(self) -> str:
        """
        Executes the SAVE command.

        Returns:
            str: "OK" to confirm the data has been saved.
        """
        REDIS_DB.dump_data()
        return "OK"

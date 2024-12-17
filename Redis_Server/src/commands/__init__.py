"""
This module provides a function to resolve Redis-like commands to their corresponding
command handler classes. It maps command strings (e.g., 'GET', 'SET') to handler classes
that implement the respective Redis command logic.

Exports:
    - get_command_handler: Resolves a given command string to its handler class.

Raises:
    - UnknownCommandException: If the command is not supported.
"""

from src.commands.base_command import RedisCommand
from src.commands.key_value_commands import (
    DecrByCommand,
    DecrCommand,
    DeleteCommand,
    ExistsCommand,
    GetCommand,
    IncrByCommand,
    IncrCommand,
    SetCommand,
)
from src.commands.list_commands import LPushCommand, RPushCommand
from src.commands.utility_commands import (
    EchoCommand,
    PingCommand,
    SaveCommand,
)
from src.exceptions.redis_exceptions import UnknownCommandException

COMMAND_MAP = {
    "PING": PingCommand,
    "ECHO": EchoCommand,
    "GET": GetCommand,
    "SET": SetCommand,
    "EXISTS": ExistsCommand,
    "DEL": DeleteCommand,
    "INCRBY": IncrByCommand,
    "INCR": IncrCommand,
    "DECR": DecrCommand,
    "DECRBY": DecrByCommand,
    "LPUSH": LPushCommand,
    "RPUSH": RPushCommand,
    "SAVE": SaveCommand,
}


def get_command_handler(command: str) -> RedisCommand:
    """
    Retrieves the corresponding Redis command handler class for a given command.

    This function serves as the central dispatcher for Redis-like commands. It maps
    command strings (e.g., 'PING', 'GET', 'SET') to their corresponding handler classes,
    which implement the required logic.

    Args:
        command (str): The command string (case-insensitive) received from the client.

    Returns:
        RedisCommand: The corresponding command handler class.

    Raises:
        UnknownCommandException: If the command is None, empty, or not supported.

    Example:
        >>> handler = get_command_handler("PING")
        >>> command_instance = handler([])  # Pass command arguments if any
        >>> command_instance.execute()
        'PONG'
    """
    if not command or not isinstance(command, str):
        raise UnknownCommandException(
            "ERR Unsupported command `None` or invalid input")

    command_cls = COMMAND_MAP.get(command.upper())
    if not command_cls:
        raise UnknownCommandException(f"ERR Unsupported command `{command}`")
    return command_cls

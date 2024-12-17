"""
This module defines the abstract base class `RedisCommand`, 
which serves as the foundation for all Redis commands.

It provides:
- Argument and option parsing logic.
- A blueprint (`execute`) for command execution, enforced by subclasses.
"""

from abc import ABC, abstractmethod
from typing import Any, List, Dict, Tuple

from src.exceptions.redis_exceptions import InvalidCommandSyntaxError



class RedisCommand(ABC):
    """
    Abstract base class for all Redis commands.

    This class provides basic functionality to:
    - Parse required arguments and optional key-value options.
    - Store parsed values in a structured format for subclasses to use.

    Subclasses must define:
        - REQUIRED_ATTRIBUTES: Tuple of required argument names.
        - POSSIBLE_OPTIONS: Tuple of valid options for the command.
        - `execute` method: To implement command-specific behavior.
    """

    REQUIRED_ATTRIBUTES: Tuple[str, ...]
    POSSIBLE_OPTIONS: Tuple[str, ...]

    def __init__(self, arguments: List[str]):
        """
        Initializes the RedisCommand with raw arguments.

        Args:
            arguments (List[str]): List of arguments passed to the command.
        """
        self._arguments: List[str] = arguments
        self._attributes: Dict[str, Any] = {}
        self._parse_arguments()

    def _parse_arguments(self) -> None:
        """
        Parses the arguments and options.

        Raises:
            InvalidCommandSyntaxError: If the number of arguments or options are invalid.
        """
        arguments = self._arguments

        if len(arguments) < len(self.REQUIRED_ATTRIBUTES):
            raise InvalidCommandSyntaxError(
                "ERR wrong number of arguments for command")

        
        idx = 0
        for key in self.REQUIRED_ATTRIBUTES:
            self._attributes[key] = arguments[idx]
            idx += 1

        if (len(arguments) - idx) % 2 != 0:
            raise InvalidCommandSyntaxError("ERR syntax error")

        for i in range(idx, len(arguments), 2):
            option = arguments[i]
            if option not in self.POSSIBLE_OPTIONS:
                raise InvalidCommandSyntaxError(
                    f"ERR invalid option: {option}")
            self._attributes[option] = arguments[i + 1]

    def get(self, key: str) -> Any:
        """
        Retrieves the value for a given argument or option.

        Args:
            key (str): The argument/option key to retrieve.

        Returns:
            Any: The value associated with the key, or None if the key does not exist.
        """
        return self._attributes.get(key)

    @abstractmethod
    def execute(self) -> str:
        """
        Abstract method to execute the Redis command.

        Subclasses must implement this method to define the behavior of the command.

        Returns:
            str: The result of executing the command.
        """
        pass

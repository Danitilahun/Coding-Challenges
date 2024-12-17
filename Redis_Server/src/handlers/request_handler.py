"""
This module handles the processing of incoming Redis-like client requests. It parses 
the RESP (Redis Serialization Protocol) data, identifies the appropriate command handler, 
and executes the command to generate a response.

It includes robust error handling for Redis-specific exceptions to ensure reliable 
request processing.

Functions:
    - process_request: Main entry point for handling client requests.
    - _handle_request: Internal function to parse and execute the command.
"""

import logging

from src.commands import get_command_handler
from src.exceptions.redis_exceptions import RedisServerException
from src.redis_protocol.deserialization_handler import RespDeserializer
from src.redis_protocol.serialization_handler import RespSerializer


logger = logging.getLogger(__name__)


def _handle_request(data: bytes) -> list:
    """
    Parse and execute a Redis command based on incoming RESP data.

    Args:
        data (bytes): The raw RESP-encoded request data from the client.

    Returns:
        list: The result of executing the Redis command.

    Raises:
        RedisServerException: If an error occurs during command execution.
    """

    command, *arguments = RespDeserializer(data=data).deserialize()

    command_handler = get_command_handler(command)

    return command_handler(arguments).execute()


def process_request(request: bytes) -> bytes:
    """
    Process a Redis-like client request and return a serialized response.

    Args:
        request (bytes): The raw RESP-encoded request data from the client.

    Returns:
        bytes: The RESP-encoded response data.
    """
    try:
        response = _handle_request(request)
        return RespSerializer().serialize(response, use_bulk=True)
    except RedisServerException as exc:
        logger.exception("Redis exception - %s", exc)
        return RespSerializer().serialize(str(exc), is_error=True)

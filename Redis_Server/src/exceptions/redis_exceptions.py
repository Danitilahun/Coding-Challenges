"""
This module defines custom exceptions for handling errors
related to Redis server operations and the Redis Serialization Protocol (RESP).

RESP (Redis Serialization Protocol) is the communication protocol used by Redis
to encode and decode client-server interactions. These exceptions handle issues
arising during RESP parsing, command processing, or protocol violations.
"""


class RedisServerException(Exception):
    """
    Base exception for all Redis server-related errors.
    """
    pass


class UnknownCommandException(RedisServerException):
    """
    Raised when a client sends an unknown command to the Redis server.
    """
    pass


class InvalidCommandSyntaxError(RedisServerException):
    """
    Raised when a command sent by the client has invalid syntax.
    """
    pass


class RespProtocolError(RedisServerException):
    """
    Raised when a RESP message violates the protocol.
    """
    pass


class RespParsingError(RedisServerException):
    """
    Raised when a RESP message cannot be parsed.
    """
    pass


class CommandProcessingException(RedisServerException):
    """
    Raised when an error occurs while processing a valid Redis command.
    """
    pass

class RespSerializationError(RedisServerException):
    """
    Raised when serialization of data into RESP format fails.
    """
    pass
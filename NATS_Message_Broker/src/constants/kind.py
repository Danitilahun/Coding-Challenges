"""
This module defines the Kind enum, which represents the types of commands
or messages in the NATS protocol.

Example:
    - Kind.CONNECT: Indicates a connection request.
    - Kind.PING: Indicates a keep-alive ping request.
"""

from enum import Enum

class Kind(Enum):
    """
    Represents the types of messages or commands handled by the NATS broker.

    Usage:
        - CONNECT: Establish a connection between client and server.
        - PING: Client sends a ping to check if the server is alive.
        - PONG: Server responds to a PING to acknowledge the connection.
        - SUB: Client subscribes to a topic.
        - PUB: Client publishes a message to a topic.
        - UNSUB: Client unsubscribes from a topic.
    """
    CONNECT = 1
    PING = 2
    PONG = 3
    SUB = 4
    PUB = 5
    UNSUB = 6

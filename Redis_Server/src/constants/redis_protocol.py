"""
This module contains constants related to the Redis Serialization Protocol (RESP).
RESP is the communication protocol used by Redis for client-server interactions.
These constants define critical elements of RESP to ensure consistency and reusability
across the project.

Constants:
    - CRLF: 
        Carriage Return Line Feed (binary format). It is used as the line terminator
        in RESP to separate different parts of a message or mark its end.
        Example: "+OK\r\n" (a Simple String response).

    - CRLF_STR: 
        Carriage Return Line Feed (string format). This is the text-based equivalent
        of CRLF, used primarily for logging or debugging when working with RESP strings.
        Example: "\r\n".

    - DEFAULT_ENCODING: 
        Specifies the encoding to be used for RESP strings. Redis uses UTF-8 by default
        to support a wide range of characters and symbols.

    - MAX_BUFFER_SIZE: 
        The maximum size (in bytes) for reading data from a socket in one operation. 
        This prevents excessive memory usage during communication.

    - DEFAULT_REDIS_PORT: 
        The default port (6379) used by Redis servers for listening to incoming connections.
        This can be overridden if Redis is configured to use a different port.
"""

CRLF = b"\r\n"

CRLF_STR = "\r\n"

DEFAULT_ENCODING = "utf-8"

MAX_BUFFER_SIZE = 1024

DEFAULT_REDIS_PORT = 6379

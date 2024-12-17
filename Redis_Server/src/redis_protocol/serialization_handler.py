"""
This module provides the `RespSerializer` class for serializing Python objects
into Redis Serialization Protocol (RESP) format. RESP is the protocol used by
Redis to encode messages between the client and server for communication.

Features:
    - Serialization of Simple Strings, Errors, Integers, Bulk Strings, and Arrays.
    - Supports flexible options for custom encoding and error handling.

RESP Format:
    - Simple Strings: Prefix with '+' (e.g., "+OK\r\n")
    - Errors: Prefix with '-' (e.g., "-Error message\r\n")
    - Integers: Prefix with ':' (e.g., ":1000\r\n")
    - Bulk Strings: Prefix with '$', followed by the length (e.g., "$6\r\nfoobar\r\n")
    - Arrays: Prefix with '*', followed by the number of elements
              (e.g., "*2\r\n$3\r\nfoo\r\n$3\r\nbar\r\n")

This implementation uses constants for protocol-specific terminators (CRLF) and
supports exceptions for custom error handling.
"""

from src.constants.redis_protocol import CRLF_STR, DEFAULT_ENCODING
from src.exceptions.redis_exceptions import RespSerializationError


class RespSerializer:
    """
    A class to serialize Python objects into RESP-compliant byte strings.

    Attributes:
        - encoding (str): Encoding used for string serialization (default: 'utf-8').
    """

    def __init__(self, encoding: str = DEFAULT_ENCODING):
        """
        Initializes the RespSerializer with the specified encoding.

        Args:
            encoding (str): Encoding used for serializing RESP strings.
                            Default is 'utf-8'.
        """
        self.encoding = encoding

    def serialize(self, data, use_bulk: bool = True, is_error: bool = False) -> bytes:
        """
        Serializes Python data into RESP-compliant byte strings.

        Args:
            data: The Python object to serialize (e.g., str, int, list, None).
            use_bulk (bool): Whether to serialize strings as Bulk Strings (default: True).
            is_error (bool): Whether to serialize the response as an error (default: False).

        Returns:
            bytes: The serialized RESP-compliant byte string.

        Raises:
            RespSerializationError: If serialization fails due to unsupported data types.
        """
        try:
            serialized_data = self._serialize(data, use_bulk, is_error)
            return serialized_data.encode(self.encoding)
        except Exception as e:
            raise RespSerializationError(f"Serialization failed: {e}") from e

    def _serialize(self, data, use_bulk: bool, is_error: bool) -> str:
        """
        Internal helper to generate RESP strings without encoding into bytes.

        Args:
            data: The Python object to serialize (e.g., str, int, list, None).
            use_bulk (bool): Whether to serialize strings as Bulk Strings.
            is_error (bool): Whether to serialize the response as an error.

        Returns:
            str: The RESP-compliant string representation of the data.

        Raises:
            RespSerializationError: If the data type is unsupported.
        """
        if is_error:
            return f"-{data}{CRLF_STR}"
        if data is None:
            return f"$-1{CRLF_STR}"
        if isinstance(data, str):
            return f"+{data}{CRLF_STR}" if not use_bulk else f"${len(data)}{CRLF_STR}{data}{CRLF_STR}"
        if isinstance(data, int):
            return f":{data}{CRLF_STR}"
        if isinstance(data, (list, tuple)):
            elements = [self._serialize(item, use_bulk, False) for item in data]
            return f"*{len(data)}{CRLF_STR}" + "".join(elements)
        raise RespSerializationError(f"Unsupported RESP type: {type(data)}, {data}")


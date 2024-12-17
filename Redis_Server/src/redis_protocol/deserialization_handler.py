"""
This module provides the `RespDeserializer` class for converting RESP (Redis Serialization Protocol)
messages into Python objects. RESP is used by Redis to encode and decode client-server interactions.

The deserialization process supports:
    - Simple Strings
    - Errors
    - Integers
    - Bulk Strings (including null bulk strings)
    - Arrays (including nested arrays)
"""

import io
from typing import Any
from src.constants.redis_protocol import CRLF, DEFAULT_ENCODING
from src.exceptions.redis_exceptions import RespParsingError, RespProtocolError


class RespDeserializer:

    def __init__(self, data: bytes, encoding: str = DEFAULT_ENCODING):
        """
        Initializes the deserializer with the given RESP data.

        Args:
            data (bytes): The RESP data to parse.
            encoding (str): The encoding used for decoding strings (default: UTF-8).
        """
        self._buffer = io.BytesIO(data)
        self._encoding = encoding

    def _readline(self) -> bytes:
        """
        Reads a single RESP line from the buffer, ensuring it ends with CRLF.
        Raises:
            RespParsingError: If incomplete RESP data is detected.
        """
        data = self._buffer.readline()
        if not data:
            raise RespParsingError(
                "Unexpected end of input while reading line")

        if not data.endswith(CRLF):
            remaining_data = self._buffer.readline()
            if not remaining_data:
                raise RespParsingError("Incomplete RESP data")
            data += remaining_data
        return data

    def _decode(self, data: bytes) -> str:
        """
        Decodes RESP data by stripping CRLF and converting to a string.

        Args:
            data (bytes): The RESP line to decode.

        Returns:
            str: The decoded string.
        """
        return data.rstrip(CRLF).decode(self._encoding)

    def deserialize(self) -> Any:
        """
        Deserializes RESP data into a Python object.
        """

        def parse_simple_string() -> str:
            return self._decode(self._readline())

        def parse_error() -> str:
            return self._decode(self._readline())

        def parse_integer() -> int:
            return int(self._decode(self._readline()))

        def parse_bulk_string() -> str:
            length = int(self._decode(self._readline()))
            if length == -1:
                return None
            return self._decode(self._buffer.read(length + len(CRLF)))

        def parse_array() -> list[Any]:
            length_line = self._readline()
            try:
                length = int(self._decode(length_line))
            except ValueError as ve:
                raise RespParsingError(f"Invalid array length: {length_line}") from ve
            
            if length == -1:
                return None
            return [self.deserialize() for _ in range(length)]

        resp_type = self._buffer.read(1)
        try:
            if resp_type == b"+":
                return parse_simple_string()
            if resp_type == b"-":
                return parse_error()
            if resp_type == b":":
                return parse_integer()
            if resp_type == b"$":
                return parse_bulk_string()
            if resp_type == b"*":
                return parse_array()
        except Exception as e:
            raise RespParsingError(
                f"Failed to parse RESP data starting with: {resp_type} - {e}"
            ) from e
        raise RespProtocolError(f"Unsupported RESP type: {resp_type}")


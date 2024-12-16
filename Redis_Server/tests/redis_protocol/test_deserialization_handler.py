"""
Unit tests for the RespDeserializer class in deserializer.py.
Tests deserialization of various RESP formats, including Simple Strings,
Errors, Integers, Bulk Strings, Null Bulk Strings, and Arrays.
"""

import unittest
from src.redis_protocol.deserialization_handler import RespDeserializer
from src.exceptions.redis_exceptions import RespParsingError, RespProtocolError


class TestRespDeserializer(unittest.TestCase):
    """
    Unit test class for RespDeserializer.
    """

    def test_simple_string(self):
        """
        Test deserialization of a Simple String.
        """
        data = b"+OK\r\n"
        deserializer = RespDeserializer(data)
        result = deserializer.deserialize()
        self.assertEqual(result, "OK")

    def test_error_string(self):
        """
        Test deserialization of an Error response.
        """
        data = b"-Error message\r\n"
        deserializer = RespDeserializer(data)
        result = deserializer.deserialize()
        self.assertEqual(result, "Error message")

    def test_integer(self):
        """
        Test deserialization of an Integer.
        """
        data = b":1000\r\n"
        deserializer = RespDeserializer(data)
        result = deserializer.deserialize()
        self.assertEqual(result, 1000)

    def test_bulk_string(self):
        """
        Test deserialization of a Bulk String.
        """
        data = b"$11\r\nhello world\r\n"
        deserializer = RespDeserializer(data)
        result = deserializer.deserialize()
        self.assertEqual(result, "hello world")

    def test_null_bulk_string(self):
        """
        Test deserialization of a Null Bulk String.
        """
        data = b"$-1\r\n"
        deserializer = RespDeserializer(data)
        result = deserializer.deserialize()
        self.assertIsNone(result)

    def test_array(self):
        """
        Test deserialization of an Array.
        """
        data = b"*2\r\n$3\r\nfoo\r\n$3\r\nbar\r\n"
        deserializer = RespDeserializer(data)
        result = deserializer.deserialize()
        self.assertEqual(result, ["foo", "bar"])

    def test_nested_array(self):
        """
        Test deserialization of a nested Array.
        """
        data = b"*3\r\n$3\r\nfoo\r\n*2\r\n$3\r\nbar\r\n$3\r\nbaz\r\n$3\r\nqux\r\n"
        deserializer = RespDeserializer(data)
        result = deserializer.deserialize()
        self.assertEqual(result, ["foo", ["bar", "baz"], "qux"])

    def test_protocol_error(self):
        """
        Test deserialization with an unsupported RESP type.
        """
        data = b"~5\r\nhello\r\n"
        deserializer = RespDeserializer(data)
        with self.assertRaises(RespProtocolError):
            deserializer.deserialize()


if __name__ == '__main__':
    unittest.main()

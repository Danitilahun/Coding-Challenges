"""
Unit tests for the RespSerializer class in serialization_handler.py.
Tests serialization of different RESP formats including Simple Strings,
Errors, Integers, Bulk Strings, Arrays, and Null values.
"""

import unittest
from src.redis_protocol.serialization_handler import RespSerializer
from src.exceptions.redis_exceptions import RespSerializationError


class TestRespSerializer(unittest.TestCase):

    def setUp(self):
        """
        Create a RespSerializer instance for testing.
        """
        self.serializer = RespSerializer()

    def test_simple_string(self):
        """
        Test serialization of a Simple String.
        """
        result = self.serializer.serialize("OK", use_bulk=False)
        self.assertEqual(result, b'+OK\r\n')

    def test_error_string(self):
        """
        Test serialization of an Error response.
        """
        result = self.serializer.serialize("Invalid command", is_error=True)
        self.assertEqual(result, b'-Invalid command\r\n')

    def test_integer(self):
        """
        Test serialization of an Integer.
        """
        result = self.serializer.serialize(42)
        self.assertEqual(result, b':42\r\n')

    def test_bulk_string(self):
        """
        Test serialization of a Bulk String.
        """
        result = self.serializer.serialize("Hello, World!")
        self.assertEqual(result, b'$13\r\nHello, World!\r\n')

    def test_null_bulk_string(self):
        """
        Test serialization of a Null Bulk String.
        """
        result = self.serializer.serialize(None)
        self.assertEqual(result, b'$-1\r\n')

    def test_array(self):
        """
        Test serialization of an Array.
        """
        result = self.serializer.serialize(["PING", "PONG"])
        self.assertEqual(result, b'*2\r\n$4\r\nPING\r\n$4\r\nPONG\r\n')

    def test_nested_array(self):
        """
        Test serialization of a nested Array.
        """
        result = self.serializer.serialize(["SET", "key", "value", ["inner"]])
        self.assertEqual(
            result,
            b'*4\r\n$3\r\nSET\r\n$3\r\nkey\r\n$5\r\nvalue\r\n*1\r\n$5\r\ninner\r\n'
        )

    def test_unsupported_type(self):
        """
        Test serialization of unsupported data types.
        """
        with self.assertRaises(RespSerializationError) as context:
            self.serializer.serialize({"key": "value"})
        self.assertIn("Unsupported RESP type", str(context.exception))


if __name__ == '__main__':
    unittest.main()

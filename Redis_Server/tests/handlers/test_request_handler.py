import unittest
from src.handlers.request_handler import process_request


class TestRequestHandler(unittest.TestCase):
    """
    Test the end-to-end Redis request handler, including RESP serialization/deserialization.
    """

    def test_ping_command(self):
        """Test PING command with RESP input."""
        raw_request = b"*1\r\n$4\r\nPING\r\n"
        response = process_request(raw_request)
        self.assertEqual(response, b'$4\r\nPONG\r\n')

    def test_echo_command(self):
        """Test ECHO command with RESP input."""
        raw_request = b"*2\r\n$4\r\nECHO\r\n$11\r\nHello World\r\n"
        response = process_request(raw_request)
        self.assertEqual(response, b"$11\r\nHello World\r\n")

    def test_set_and_get_command(self):
        """Test SET and GET commands with RESP input."""
        set_request = b"*3\r\n$3\r\nSET\r\n$5\r\nmykey\r\n$7\r\nmyvalue\r\n"
        get_request = b"*2\r\n$3\r\nGET\r\n$5\r\nmykey\r\n"

        set_response = process_request(set_request)
        get_response = process_request(get_request)

        self.assertEqual(set_response, b'$2\r\nOK\r\n')
        self.assertEqual(get_response, b"$7\r\nmyvalue\r\n")

    def test_delete_command(self):
        """Test DELETE command with RESP input."""
        process_request(b"*3\r\n$3\r\nSET\r\n$4\r\nkey1\r\n$6\r\nvalue1\r\n")
        process_request(b"*3\r\n$3\r\nSET\r\n$4\r\nkey2\r\n$6\r\nvalue2\r\n")
        delete_request = b"*3\r\n$3\r\nDEL\r\n$4\r\nkey1\r\n$4\r\nkey2\r\n"

        response = process_request(delete_request)
        self.assertEqual(response, b":2\r\n")


if __name__ == "__main__":
    unittest.main()

import unittest
import socket
import threading
import time

from server import start_server


class TestRedisLikeServer(unittest.TestCase):
    HOST = "127.0.0.1"
    PORT = 6380

    @classmethod
    def setUpClass(cls):
        """Start the Redis-like server in a separate thread for testing."""
        cls.server_thread = threading.Thread(
            target=start_server, args=(cls.HOST, cls.PORT), daemon=True
        )
        cls.server_thread.start()
        time.sleep(1)  # Allow server time to start

    def send_command(self, command: bytes) -> str:
        """
        Helper function to send a RESP-encoded command to the server
        and receive its response.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((self.HOST, self.PORT))
            client_socket.sendall(command)
            response = client_socket.recv(1024)
            return response.decode()

    def test_ping_command(self):
        """Test PING command."""
        response = self.send_command(b"*1\r\n$4\r\nPING\r\n")
        self.assertEqual(response, "$4\r\nPONG\r\n")

    def test_echo_command(self):
        """Test ECHO command."""
        response = self.send_command(b"*2\r\n$4\r\nECHO\r\n$11\r\nHello World\r\n")
        self.assertEqual(response, "$11\r\nHello World\r\n")

    def test_set_and_get_command(self):
        """Test SET and GET commands."""
        set_response = self.send_command(b"*3\r\n$3\r\nSET\r\n$3\r\nkey\r\n$5\r\nvalue\r\n")
        self.assertEqual(set_response, "$2\r\nOK\r\n")

        get_response = self.send_command(b"*2\r\n$3\r\nGET\r\n$3\r\nkey\r\n")
        self.assertEqual(get_response, "$5\r\nvalue\r\n")

    def test_delete_command(self):
        """Test DELETE command."""
        self.send_command(b"*3\r\n$3\r\nSET\r\n$4\r\nkey1\r\n$5\r\nvalue\r\n")
        response = self.send_command(b"*2\r\n$3\r\nDEL\r\n$4\r\nkey1\r\n")
        self.assertEqual(response, ":1\r\n")

    def test_exists_command(self):
        """Test EXISTS command."""
        self.send_command(b"*3\r\n$3\r\nSET\r\n$4\r\nkey1\r\n$5\r\nvalue\r\n")
        response = self.send_command(b"*2\r\n$6\r\nEXISTS\r\n$4\r\nkey1\r\n")
        self.assertEqual(response, ":1\r\n")

    def test_incr_command(self):
        """Test INCR command."""
        self.send_command(b"*3\r\n$3\r\nSET\r\n$3\r\nnum\r\n$1\r\n0\r\n")
        response = self.send_command(b"*2\r\n$4\r\nINCR\r\n$3\r\nnum\r\n")
        self.assertEqual(response, ":1\r\n")

    def test_decr_command(self):
        """Test DECR command."""
        self.send_command(b"*3\r\n$3\r\nSET\r\n$3\r\nnum\r\n$1\r\n2\r\n")
        response = self.send_command(b"*2\r\n$4\r\nDECR\r\n$3\r\nnum\r\n")
        self.assertEqual(response, ":1\r\n")

    def test_lpush_and_rpush_command(self):
        """Test LPUSH and RPUSH commands."""
        lpush_response = self.send_command(b"*4\r\n$5\r\nLPUSH\r\n$5\r\nlist1\r\n$1\r\nA\r\n$1\r\nB\r\n")
        self.assertEqual(lpush_response, ":2\r\n")

        rpush_response = self.send_command(b"*4\r\n$5\r\nRPUSH\r\n$5\r\nlist1\r\n$1\r\nC\r\n$1\r\nD\r\n")
        self.assertEqual(rpush_response, ":4\r\n")

    def test_save_command(self):
        """Test SAVE command."""
        response = self.send_command(b"*1\r\n$4\r\nSAVE\r\n")
        self.assertEqual(response, "$2\r\nOK\r\n")


if __name__ == "__main__":
    unittest.main()

import unittest
from unittest.mock import Mock
from src.protocols.parser import Parser
from src.constants.state import State
from src.constants.kind import Kind
from src.messages.message import Message
from src.messages.args import PubArg


class TestParser(unittest.TestCase):
    def setUp(self):
        """
        Set up a mock callback and a Parser instance for testing.
        """
        self.mock_cb = Mock()
        self.parser = Parser(cb=self.mock_cb)

    def test_ping_command(self):
        """
        Test parsing the PING command.
        """
        self.parser.parse(b"PING\r\n")
        self.mock_cb.assert_called_once_with(Message(kind=Kind.PING))
        self.assertEqual(self.parser.state, State.OP_START)

    def test_pong_command(self):
        """
        Test parsing the PONG command.
        """
        self.parser.parse(b"PONG\r\n")
        self.mock_cb.assert_called_once_with(Message(kind=Kind.PONG))
        self.assertEqual(self.parser.state, State.OP_START)

    def test_connect_command(self):
        """
        Test parsing the CONNECT command with arguments.
        """
        self.parser.parse(b"CONNECT {\"verbose\":true}\r\n")
        self.mock_cb.assert_called_once_with(
            Message(kind=Kind.CONNECT, data=b"{\"verbose\":true}")
        )
        self.assertEqual(self.parser.state, State.OP_START)

    def test_pub_command(self):
        """
        Test parsing the PUB command with payload.
        """
        data = b"PUB foo.bar 5\r\nhello\r\n"
        self.parser.parse(data)

        expected_pub_arg = PubArg(
            subject=b"foo.bar", reply_to=None, payload_size=5, payload=b"hello"
        )
        self.mock_cb.assert_called_once_with(Message(kind=Kind.PUB, pub_arg=expected_pub_arg))
        self.assertEqual(self.parser.state, State.OP_START)

    def test_pub_command_split_payload(self):
        """
        Test parsing a PUB command when the payload is split across buffers.
        """
        self.parser.parse(b"PUB foo.bar 5\r\nhel")
        self.parser.parse(b"lo\r\n")

        expected_pub_arg = PubArg(
            subject=b"foo.bar", reply_to=None, payload_size=5, payload=b"hello"
        )
        self.mock_cb.assert_called_once_with(Message(kind=Kind.PUB, pub_arg=expected_pub_arg))
        self.assertEqual(self.parser.state, State.OP_START)

    def test_invalid_command(self):
        """
        Test handling of an invalid command.
        """
        with self.assertRaises(Exception) as context:
            self.parser.parse(b"INVALID\r\n")
        self.assertIn("Parsing error", str(context.exception))

    def test_partial_buffer_ping(self):
        """
        Test parsing a partial buffer for PING command.
        """
        self.parser.parse(b"PIN")
        self.assertEqual(self.parser.state, State.OP_PIN)

        self.parser.parse(b"G\r\n")
        self.mock_cb.assert_called_once_with(Message(kind=Kind.PING))
        self.assertEqual(self.parser.state, State.OP_START)

    def test_multiple_commands_in_one_buffer(self):
        """
        Test parsing multiple commands in a single buffer.
        """
        self.parser.parse(b"PING\r\nPONG\r\n")
        self.mock_cb.assert_any_call(Message(kind=Kind.PING))
        self.mock_cb.assert_any_call(Message(kind=Kind.PONG))
        self.assertEqual(self.mock_cb.call_count, 2)
        self.assertEqual(self.parser.state, State.OP_START)

    def test_pub_with_large_payload(self):
        """
        Test parsing a PUB command with a large payload.
        """
        payload = b"a" * 1024
        command = f"PUB foo.bar {len(payload)}\r\n".encode() + payload + b"\r\n"
        self.parser.parse(command)

        expected_pub_arg = PubArg(
            subject=b"foo.bar", reply_to=None, payload_size=1024, payload=payload
        )
        self.mock_cb.assert_called_once_with(Message(kind=Kind.PUB, pub_arg=expected_pub_arg))
        self.assertEqual(self.parser.state, State.OP_START)

    def test_process_invalid_state(self):
        """
        Test parser behavior when in an unknown state.
        """
        self.parser.state = "INVALID_STATE"
        with self.assertRaises(Exception) as context:
            self.parser.parse(b"PING\r\n")
        self.assertIn("Parsing error", str(context.exception))


    def test_sub_command(self):
        """
        Test parsing the SUB command with a subject and queue group.
        """
        self.parser.parse(b"SUB foo.bar group1\r\n")
        self.mock_cb.assert_called_once_with(
            Message(kind=Kind.SUB, data=b"foo.bar group1")
        )
        self.assertEqual(self.parser.state, State.OP_START)

    def test_sub_command_no_queue(self):
        """
        Test parsing the SUB command with a subject but no queue group.
        """
        self.parser.parse(b"SUB foo.bar\r\n")
        self.mock_cb.assert_called_once_with(
            Message(kind=Kind.SUB, data=b"foo.bar")
        )
        self.assertEqual(self.parser.state, State.OP_START)


if __name__ == "__main__":
    unittest.main()

import unittest
from src.commands import get_command_handler
from src.commands.utility_commands import PingCommand, EchoCommand, SaveCommand
from src.commands.key_value_commands import GetCommand, SetCommand, IncrCommand, DecrByCommand
from src.commands.list_commands import LPushCommand, RPushCommand
from src.exceptions.redis_exceptions import UnknownCommandException


class TestCommandHandler(unittest.TestCase):
    """
    Unit tests for the get_command_handler function in command_handler.py.
    """

    def test_valid_command(self):
        """Test that get_command_handler returns the correct handler for valid commands."""
        self.assertEqual(get_command_handler("PING"), PingCommand)
        self.assertEqual(get_command_handler("ECHO"), EchoCommand)
        self.assertEqual(get_command_handler("SAVE"), SaveCommand)
        self.assertEqual(get_command_handler("GET"), GetCommand)
        self.assertEqual(get_command_handler("SET"), SetCommand)
        self.assertEqual(get_command_handler("INCR"), IncrCommand)
        self.assertEqual(get_command_handler("DECRBY"), DecrByCommand)
        self.assertEqual(get_command_handler("LPUSH"), LPushCommand)
        self.assertEqual(get_command_handler("RPUSH"), RPushCommand)

    def test_case_insensitivity(self):
        """Test that get_command_handler works with commands in different cases."""
        self.assertEqual(get_command_handler("ping"), PingCommand)
        self.assertEqual(get_command_handler("Ping"), PingCommand)
        self.assertEqual(get_command_handler("eChO"), EchoCommand)
        self.assertEqual(get_command_handler("SET"), SetCommand)
        self.assertEqual(get_command_handler("lpush"), LPushCommand)

    def test_unknown_command(self):
        """Test that get_command_handler raises UnknownCommandException for invalid commands."""
        with self.assertRaises(UnknownCommandException) as context:
            get_command_handler("UNKNOWN")
        self.assertEqual(
            str(context.exception),
            "ERR Unsupported command `UNKNOWN`"
        )

        with self.assertRaises(UnknownCommandException):
            get_command_handler("INVALIDCOMMAND")

        with self.assertRaises(UnknownCommandException):
            get_command_handler("")

    def test_edge_cases(self):
        """Test edge cases like None or invalid inputs."""
        with self.assertRaises(UnknownCommandException):
            get_command_handler(None)

        with self.assertRaises(UnknownCommandException):
            get_command_handler("   ")



if __name__ == "__main__":
    unittest.main()

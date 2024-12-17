
from unittest.mock import patch
import unittest

from src.commands.utility_commands import EchoCommand, PingCommand, SaveCommand
from src.redisDB.redis_db import RedisDB

class TestUtilityCommands(unittest.TestCase):
    def test_ping_command(self):
        command = PingCommand([])
        self.assertEqual(command.execute(), "PONG")

    def test_echo_command_with_arguments(self):
        command = EchoCommand(["Hello", "World"])
        self.assertEqual(command.execute(), "Hello World")

    def test_echo_command_no_arguments(self):
        command = EchoCommand([])
        self.assertEqual(command.execute(), "")


if __name__ == "__main__":
    unittest.main()

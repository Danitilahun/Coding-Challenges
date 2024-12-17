import unittest
from collections import deque
from unittest.mock import patch
from src.commands.list_commands import LPushCommand, RPushCommand
from src.redisDB.redis_db import RedisDB


class TestListCommands(unittest.TestCase):
    """
    Unit tests for LPushCommand and RPushCommand.
    """

    def setUp(self):
        """
        Set up a fresh RedisDB instance for each test.
        """
        self.mock_db = RedisDB("test_snapshot.pkl")
        self.mock_db._data = {}  # Clear in-memory data

        # Patch REDIS_DB in list_commands.py
        patcher = patch("src.commands.list_commands.REDIS_DB", self.mock_db)
        self.addCleanup(patcher.stop)
        patcher.start()

    def test_lpush_command_new_list(self):
        """Test LPushCommand adds values to a new list."""
        command = LPushCommand(["mylist", "A", "B", "C"])
        result = command.execute()
        self.assertEqual(result, 3)

        self.assertEqual(self.mock_db.get("mylist")[0], deque(["C", "B", "A"]))

    def test_rpush_command_new_list(self):
        """Test RPushCommand adds values to a new list."""
        command = RPushCommand(["mylist", "1", "2", "3"])
        result = command.execute()
        self.assertEqual(result, 3)

        self.assertEqual(self.mock_db.get("mylist")[0], deque(["1", "2", "3"]))


if __name__ == "__main__":
    unittest.main()

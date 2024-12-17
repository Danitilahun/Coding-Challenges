import unittest
from unittest.mock import patch
from src.commands.key_value_commands import (
    GetCommand,
    SetCommand,
    DeleteCommand,
    ExistsCommand,
    IncrCommand,
    DecrCommand,
)
from src.redisDB.redis_db import RedisDB


class TestKeyValueCommands(unittest.TestCase):
    """
    Unit tests for key-value Redis commands.
    """

    def setUp(self):
        """
        Set up a fresh RedisDB instance for each test.
        """
        self.mock_db = RedisDB("test_snapshot.pkl")
        self.mock_db._data = {}

        patcher = patch("src.commands.key_value_commands.REDIS_DB", self.mock_db)
        self.addCleanup(patcher.stop)
        patcher.start()

    def test_set_command_without_expiry(self):
        """Test SetCommand sets a key without expiry."""
        command = SetCommand(["mykey", "myvalue"])
        result = command.execute()

        self.assertEqual(result, "OK")
        self.assertEqual(self.mock_db.get("mykey")[0], "myvalue")

    def test_set_command_with_expiry(self):
        """Test SetCommand sets a key with expiry (EX)."""
        command = SetCommand(["mykey", "myvalue", "EX", "10"])
        result = command.execute()

        self.assertEqual(result, "OK")
        value, expires = self.mock_db.get("mykey")
        self.assertEqual(value, "myvalue")
        self.assertIsNotNone(expires)

    def test_get_command_existing_key(self):
        """Test GetCommand retrieves the value of an existing key."""
        self.mock_db.set("mykey", ("myvalue", None))
        command = GetCommand(["mykey"])
        result = command.execute()

        self.assertEqual(result, "myvalue")

    def test_get_command_expired_key(self):
        """Test GetCommand returns None for an expired key."""
        self.mock_db.set("mykey", ("myvalue", 0))  # Expired key
        command = GetCommand(["mykey"])
        result = command.execute()

        self.assertIsNone(result)
        self.assertNotIn("mykey", self.mock_db)

    def test_delete_command(self):
        """Test DeleteCommand deletes one or more keys."""
        self.mock_db.set("key1", ("value1", None))
        self.mock_db.set("key2", ("value2", None))

        command = DeleteCommand(["key1", "key2", "key3"])
        result = command.execute()

        self.assertEqual(result, 2)
        self.assertNotIn("key1", self.mock_db)
        self.assertNotIn("key2", self.mock_db)

    def test_exists_command(self):
        """Test ExistsCommand checks the existence of keys."""
        self.mock_db.set("key1", ("value1", None))
        self.mock_db.set("key2", ("value2", None))
        self.mock_db.set("expired_key", ("value3", 0))  # Expired key

        command = ExistsCommand(["key1", "key2", "expired_key", "nonexistent"])
        result = command.execute()

        self.assertEqual(result, 2)  # Only key1 and key2 exist

    def test_incr_command_new_key(self):
        """Test IncrCommand increments a new key."""
        command = IncrCommand(["counter"])
        result = command.execute()

        self.assertEqual(result, 1)
        self.assertEqual(self.mock_db.get("counter")[0], 1)

    def test_incr_command_existing_key(self):
        """Test IncrCommand increments an existing key."""
        self.mock_db.set("counter", ("5", None))
        command = IncrCommand(["counter"])
        result = command.execute()

        self.assertEqual(result, 6)
        self.assertEqual(self.mock_db.get("counter")[0], 6)

    def test_decr_command_new_key(self):
        """Test DecrCommand decrements a new key."""
        command = DecrCommand(["counter"])
        result = command.execute()

        self.assertEqual(result, -1)
        self.assertEqual(self.mock_db.get("counter")[0], -1)

    def test_decr_command_existing_key(self):
        """Test DecrCommand decrements an existing key."""
        self.mock_db.set("counter", ("5", None))
        command = DecrCommand(["counter"])
        result = command.execute()

        self.assertEqual(result, 4)
        self.assertEqual(self.mock_db.get("counter")[0], 4)


if __name__ == "__main__":
    unittest.main()

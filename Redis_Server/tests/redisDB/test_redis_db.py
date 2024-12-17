"""
Unit tests for the RedisDB class.
Tests include singleton behavior, data manipulation (set, get, delete),
and snapshot persistence using pickle.
"""

import unittest
import os

from src.redisDB.redis_db import RedisDB


class TestRedisDB(unittest.TestCase):
    """Unit tests for the RedisDB class."""

    TEST_SNAPSHOT_FILE = "test_redis_snapshot.pkl"

    def setUp(self):
        """
        Set up a fresh RedisDB instance with a test snapshot file before each test.
        Clears the snapshot file if it exists.
        """
        if os.path.exists(self.TEST_SNAPSHOT_FILE):
            os.remove(self.TEST_SNAPSHOT_FILE)
        self.db = RedisDB.from_file(self.TEST_SNAPSHOT_FILE)

    def tearDown(self):
        """
        Clean up after each test by deleting the test snapshot file.
        """
        if os.path.exists(self.TEST_SNAPSHOT_FILE):
            os.remove(self.TEST_SNAPSHOT_FILE)

    def test_singleton_behavior(self):
        """
        Test that RedisDB implements the singleton pattern.
        """
        db1 = RedisDB.from_file(self.TEST_SNAPSHOT_FILE)
        db2 = RedisDB.from_file(self.TEST_SNAPSHOT_FILE)
        self.assertIs(db1, db2, "RedisDB is not enforcing singleton behavior.")

    def test_set_and_get(self):
        """
        Test setting and retrieving values from the database.
        """
        self.db.set("key1", "value1")
        result = self.db.get("key1")
        self.assertEqual(result, "value1", "Set or get method failed.")

    def test_get_with_default(self):
        """
        Test retrieving a key that does not exist with a default value.
        """
        result = self.db.get("nonexistent_key", "default_value")
        self.assertEqual(result, "default_value", "Default value for get failed.")

    def test_delete_key(self):
        """
        Test deleting a key-value pair from the database.
        """
        self.db.set("key_to_delete", "value")
        self.db.delete("key_to_delete")
        self.assertNotIn("key_to_delete", self.db, "Delete method failed.")

    def test_contains_method(self):
        """
        Test the __contains__ method to check for key existence.
        """
        self.db.set("key_exists", "value")
        self.assertTrue("key_exists" in self.db, "__contains__ failed for existing key.")
        self.assertFalse("key_missing" in self.db, "__contains__ failed for missing key.")

    def test_persistence_snapshot(self):
        """
        Test saving data to a snapshot file and reloading it.
        """
        self.db.set("persistent_key", "persistent_value")
        self.db.dump_data()

        # Load a new instance from the snapshot
        new_db = RedisDB.from_file(self.TEST_SNAPSHOT_FILE)
        result = new_db.get("persistent_key")
        self.assertEqual(result, "persistent_value", "Snapshot persistence failed.")

    def test_empty_snapshot_file(self):
        """
        Test behavior when loading from a non-existent or empty snapshot file.
        """
        new_db = RedisDB.from_file("non_existent_snapshot.pkl")
        self.assertEqual(new_db.get("any_key"), None, "Loading empty snapshot failed.")


if __name__ == "__main__":
    unittest.main()

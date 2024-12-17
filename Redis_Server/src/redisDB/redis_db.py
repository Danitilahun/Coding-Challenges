"""
This module implements a lightweight in-memory key-value database with:
- Singleton Pattern to ensure only one instance exists.
- Snapshot Persistence: Data is saved to and loaded from a file using pickle.
- Factory Method: `from_file` for initializing the database from a snapshot.

Features:
- `set`: Add or update a key-value pair.
- `get`: Retrieve a value with optional default.
- `delete`: Remove a key-value pair.
- `dump_data`: Save the current state to a file.
"""

import threading
import pickle
from typing import Any, Optional


class RedisDB:
    """
    A lightweight in-memory key-value database with singleton behavior
    and snapshot persistence.
    """

    _instance_lock: threading.Lock = threading.Lock()
    _instance: Optional["RedisDB"] = None

    def __new__(cls, *args, **kwargs) -> "RedisDB":
        """
        Implements the singleton pattern to ensure only one instance of RedisDB exists.
        """
        with cls._instance_lock:
            if not cls._instance:
                cls._instance = super().__new__(cls)
            return cls._instance

    def __init__(self, snapshot_filename: str, data: Optional[dict[str, Any]] = None):
        """
        Initializes the RedisDB instance.

        Args:
            snapshot_filename (str): Path to the file for saving/loading the snapshot.
            data (Optional[dict]): Initial data for the database. Defaults to an empty dictionary.
        """
        self._snapshot_filename: str = snapshot_filename
        self._data: dict[str, Any] = data or {}

    @classmethod
    def from_file(cls, snapshot_filename: str) -> "RedisDB":
        """
        Factory method to create a RedisDB instance from a snapshot file.

        Args:
            snapshot_filename (str): Path to the snapshot file.

        Returns:
            RedisDB: An instance of RedisDB initialized with data from the file.
        """
        return cls(
            snapshot_filename=snapshot_filename,
            data=cls.load_snapshot(snapshot_filename),
        )

    @staticmethod
    def load_snapshot(snapshot_filename: str) -> dict[str, Any]:
        """
        Loads a snapshot from the specified file.

        Args:
            snapshot_filename (str): Path to the snapshot file.

        Returns:
            dict: A dictionary representing the loaded data.
        """
        try:
            with open(snapshot_filename, "rb") as file:
                return pickle.load(file)
        except FileNotFoundError:
            return {}

    def dump_data(self) -> None:
        """
        Saves the current state of the database to the snapshot file.
        """
        with open(self._snapshot_filename, "wb") as file:
            pickle.dump(self._data, file)

    def __contains__(self, key: str) -> bool:
        """
        Checks if a key exists in the database.

        Args:
            key (str): The key to check.

        Returns:
            bool: True if the key exists, False otherwise.
        """
        return key in self._data

    def __getitem__(self, item: str) -> Any:
        """
        Retrieves the value associated with the given key.

        Args:
            item (str): The key to look up.

        Returns:
            Any: The value associated with the key.
        """
        return self._data[item]

    def set(self, key: Any, value: Any) -> None:
        """
        Adds or updates a key-value pair in the database.

        Args:
            key (Any): The key to store.
            value (Any): The value to associate with the key.
        """
        self._data[key] = value

    def get(self, key: Any, default: Optional[Any] = None) -> Any:
        """
        Retrieves a value by its key, with an optional default.

        Args:
            key (Any): The key to look up.
            default (Optional[Any]): Value to return if the key does not exist.

        Returns:
            Any: The value associated with the key or the default.
        """
        return self._data.get(key, default)

    def delete(self, key: Any) -> None:
        """
        Deletes a key-value pair from the database.

        Args:
            key (Any): The key to delete.
        """
        del self._data[key]


# Initialize the RedisDB singleton instance with a snapshot file
REDIS_DB: RedisDB = RedisDB.from_file("redis_snapshot.pkl")

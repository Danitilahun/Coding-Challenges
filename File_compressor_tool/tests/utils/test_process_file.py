import os
import unittest
from unittest import mock
from hamcrest import assert_that, equal_to, calling, raises
from src.utils.file_handler import process_file

class TestProcessFile(unittest.TestCase):
    def setUp(self):
        """
        Set up a valid test file before each test.
        """
        self.test_file = "test_input.txt"
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write("Sample content")

    def tearDown(self):
        """
        Clean up test files after each test.
        """
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

        if os.path.exists("test_output.huf"):
            os.remove("test_output.huf")

    def test_process_file_valid(self):
        """
        Test that process_file correctly reads and returns the content of a valid file.
        """
        content = process_file(self.test_file)
        assert_that(content, equal_to("Sample content"))

    def test_process_file_nonexistent(self):
        """
        Test that process_file raises FileNotFoundError when the file does not exist.
        """
        nonexistent_file = "no_such_file.txt"
        assert_that(
            calling(process_file).with_args(nonexistent_file),
            raises(FileNotFoundError, f"Error: File '{nonexistent_file}' does not exist.")
        )

    def test_process_file_directory(self):
        """
        Test that process_file raises IsADirectoryError when a directory path is provided instead of a file.
        """
        directory_path = "."
        assert_that(
            calling(process_file).with_args(directory_path),
            raises(IsADirectoryError, f"Error: '{directory_path}' is not a valid file.")
        )

    def test_process_file_unicode_decode_error(self):
        """
        Test that process_file raises UnicodeDecodeError when the file contains undecodable characters.
        """
        # Create a file with invalid UTF-8 bytes
        invalid_utf8_file = "invalid_utf8.txt"
        with open(invalid_utf8_file, "wb") as f:
            f.write(b'\xff\xfe\xfa')  # Invalid UTF-8 bytes

        try:
            assert_that(
                calling(process_file).with_args(invalid_utf8_file),
                raises(
                    UnicodeDecodeError,
                    f"Error: Unable to decode the file '{invalid_utf8_file}'."
                )
            )
        finally:
            if os.path.exists(invalid_utf8_file):
                os.remove(invalid_utf8_file)

    @mock.patch("builtins.open", side_effect=IOError("Permission denied"))
    def test_process_file_io_error(self, mock_open):
        """
        Test that process_file raises IOError when the file cannot be opened.
        """
        filename = self.test_file
        assert_that(
            calling(process_file).with_args(filename),
            raises(IOError, f"Error: Unable to open the file '{filename}'. Details: Permission denied")
        )

if __name__ == "__main__":
    unittest.main()

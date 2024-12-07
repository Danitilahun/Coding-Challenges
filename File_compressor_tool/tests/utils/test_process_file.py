import unittest
from typing import cast
from hamcrest import assert_that, equal_to, calling, raises
from tests.infrastructure.givenpy import given, then, when
from tests.infrastructure.steps import (
    prepare_file_system,
    create_invalid_file,
)
from src.utils.file_reader import process_file


class ProcessFileTest(unittest.TestCase):
    def test_that_valid_file_returns_content(self):
        with given([
            prepare_file_system(valid_file_content="Sample content")
        ]) as context:
            file_path = cast(str, context.file_path)

            with when():
                content = process_file(file_path)

            with then():
                assert_that(content, equal_to("Sample content"))

    def test_that_non_existent_file_raises_file_not_found_error(self):
        with given([
            prepare_file_system(non_existent_file=True)
        ]) as context:
            file_path = cast(str, context.file_path)

            with when():
                action = calling(process_file).with_args(file_path)

            with then():
                assert_that(action, raises(FileNotFoundError))

    def test_that_directory_instead_of_file_raises_is_a_directory_error(self):
        with given([
            prepare_file_system(directory_instead_of_file=True)
        ]) as context:
            file_path = cast(str, context.file_path)

            with when():
                action = calling(process_file).with_args(file_path)

            with then():
                assert_that(action, raises(IsADirectoryError))

    def test_that_unreadable_file_raises_io_error(self):
        with given([
            prepare_file_system(unreadable_file=True)
        ]) as context:
            file_path = cast(str, context.file_path)

            with when():
                action = calling(process_file).with_args(file_path)

            with then():
                assert_that(action, raises(IOError))

    def test_that_unicode_error_raises_unicode_decode_error(self):
        with given([
            prepare_file_system(invalid_file_content="\x9d")
        ]) as context:
            file_path = cast(str, context.file_path)

            with when():
                action = calling(process_file).with_args(file_path)

            with then():
                assert_that(action, raises(UnicodeDecodeError))

import unittest
from src.utils.arg_parsers import split_args, parse_sub, prepare_pub, parse_unsub_arg
from src.messages.args import SubArg, PubArg, UnsubArg


class TestArgParsers(unittest.TestCase):

    def test_split_args(self):
        """
        Test the split_args function for various inputs.
        """
        result = split_args(b"foo")
        self.assertEqual(result, [b"foo"])

        result = split_args(b"foo bar baz")
        self.assertEqual(result, [b"foo", b"bar", b"baz"])

        result = split_args(b"foo\tbar\nbaz\rqux")
        self.assertEqual(result, [b"foo", b"bar", b"baz", b"qux"])

        result = split_args(b"   foo bar   ")
        self.assertEqual(result, [b"foo", b"bar"])

        result = split_args(b"")
        self.assertEqual(result, [])

    def test_parse_sub(self):
        """
        Test the parse_sub function for different SUB command formats.
        """
        
        result = parse_sub(b"foo.bar 123")
        expected = SubArg(subject=b"foo.bar", group=None, sid=123)
        self.assertEqual(result, expected)

        result = parse_sub(b"foo.bar group 456")
        expected = SubArg(subject=b"foo.bar", group=b"group", sid=456)
        self.assertEqual(result, expected)

        with self.assertRaises(ValueError):
            parse_sub(b"foo.bar")

    def test_prepare_pub(self):
        """
        Test the prepare_pub function for different PUB command formats.
        """

        result = prepare_pub(b"foo.bar 42")
        expected = PubArg(subject=b"foo.bar", reply_to=None, payload_size=42, payload=None)
        self.assertEqual(result, expected)

        result = prepare_pub(b"foo.bar reply.to 84")
        expected = PubArg(subject=b"foo.bar", reply_to=b"reply.to", payload_size=84, payload=None)
        self.assertEqual(result, expected)

        with self.assertRaises(ValueError):
            prepare_pub(b"foo.bar")

    def test_parse_unsub_arg(self):
        """
        Test the parse_unsub_arg function for different UNSUB command formats.
        """
        
        result = parse_unsub_arg(b"123")
        expected = UnsubArg(sid=123, max_msgs=None)
        self.assertEqual(result, expected)

        result = parse_unsub_arg(b"123 10")
        expected = UnsubArg(sid=123, max_msgs=10)
        self.assertEqual(result, expected)

        with self.assertRaises(ValueError):
            parse_unsub_arg(b"")


if __name__ == "__main__":
    unittest.main()

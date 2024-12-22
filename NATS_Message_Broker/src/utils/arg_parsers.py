from typing import List
from messages.args import SubArg, PubArg, UnsubArg
from enum import IntEnum


class WhiteSpace(IntEnum):
    """
    Represents ASCII codes for whitespace characters.
    """
    SPACE = ord(' ')    # Space character
    NL = ord('\n')      # Newline character
    TAB = ord('\t')     # Tab character
    CR = ord('\r')      # Carriage return character


def split_args(data: bytes) -> List[bytes]:
    """
    Splits a buffer into a list of arguments based on whitespace.

    Whitespace characters include:
        - SPACE (' ')
        - NEWLINE ('\n')
        - TAB ('\t')
        - CARRIAGE RETURN ('\r')

    Args:
        data (bytes): The input buffer to split.

    Returns:
        List[bytes]: A list of arguments split by whitespace.
    """
    args = []
    start = -1

    for i, b in enumerate(data):
        if b in {WhiteSpace.SPACE, WhiteSpace.NL, WhiteSpace.TAB, WhiteSpace.CR}:
            if start >= 0:
                args.append(data[start:i])
                start = -1
        else:
            if start < 0:
                start = i

    # Handle the last argument if it's at the end of the buffer
    if start >= 0:
        args.append(data[start:])

    return args


def parse_sub(data: bytes) -> SubArg:
    """
    Parses arguments for the SUB command.

    The SUB command has the following formats:
        - `SUB <subject> <sid>`: No group specified.
        - `SUB <subject> <group> <sid>`: With group specified.

    Args:
        data (bytes): The raw buffer containing SUB command arguments.

    Returns:
        SubArg: A structured SubArg object containing parsed data.
    """
    args = split_args(data)

    sub_arg = SubArg(subject=b"", group=None, sid=-1)

    if len(args) == 2:
        sub_arg.subject = args[0]
        sub_arg.group = None
        sub_arg.sid = int(args[1].decode())
    elif len(args) == 3:
        sub_arg.subject = args[0]
        sub_arg.group = args[1]
        sub_arg.sid = int(args[2].decode())

    return sub_arg


def prepare_pub(data: bytes) -> PubArg:
    """
    Parses arguments for the PUB command.

    The PUB command has the following formats:
        - `PUB <subject> <size>`: Without a reply-to.
        - `PUB <subject> <reply-to> <size>`: With a reply-to.

    Args:
        data (bytes): The raw buffer containing PUB command arguments.

    Returns:
        PubArg: A structured PubArg object containing parsed data.
    """
    args = split_args(data)

    pub_arg = PubArg(subject=b"", reply_to=None, payload_size=0, payload=None)

    if len(args) == 2:
        pub_arg.subject = args[0]
        pub_arg.reply_to = None
        pub_arg.payload_size = int(args[1].decode())
    elif len(args) == 3:
        pub_arg.subject = args[0]
        pub_arg.reply_to = args[1]
        pub_arg.payload_size = int(args[2].decode())

    return pub_arg


def parse_unsub_arg(data: bytes) -> UnsubArg:
    """
    Parses arguments for the UNSUB command.

    The UNSUB command has the following formats:
        - `UNSUB <sid>`: No max messages specified.
        - `UNSUB <sid> <max_msgs>`: With max messages specified.

    Args:
        data (bytes): The raw buffer containing UNSUB command arguments.

    Returns:
        UnsubArg: A structured UnsubArg object containing parsed data.
    """
    args = split_args(data)

    unsub_arg = UnsubArg(sid=-1, max_msgs=None)

    if len(args) == 1:
        unsub_arg.sid = int(args[0].decode())
    elif len(args) == 2:
        unsub_arg.sid = int(args[0].decode())
        unsub_arg.max_msgs = int(args[1].decode())

    return unsub_arg

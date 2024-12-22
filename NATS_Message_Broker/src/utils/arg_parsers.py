from typing import List
from src.messages.args import SubArg, PubArg, UnsubArg
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

    Args:
        data (bytes): The raw buffer containing SUB command arguments.

    Returns:
        SubArg: A structured SubArg object containing parsed data.

    Raises:
        ValueError: If the input data does not match the expected format.
    """
    args = split_args(data)

    if len(args) < 2 or len(args) > 3:
        raise ValueError(f"Invalid SUB command arguments: {data}")

    sub_arg = SubArg(subject=args[0], group=None, sid=int(args[-1].decode()))
    if len(args) == 3:
        sub_arg.group = args[1]

    return sub_arg


def prepare_pub(data: bytes) -> PubArg:
    """
    Parses arguments for the PUB command.

    Args:
        data (bytes): The raw buffer containing PUB command arguments.

    Returns:
        PubArg: A structured PubArg object containing parsed data.

    Raises:
        ValueError: If the input data does not match the expected format.
    """
    args = split_args(data)

    if len(args) < 2 or len(args) > 3:
        raise ValueError(f"Invalid PUB command arguments: {data}")

    pub_arg = PubArg(
        subject=args[0],
        reply_to=args[1] if len(args) == 3 else None,
        payload_size=int(args[-1].decode())
    )

    return pub_arg


def parse_unsub_arg(data: bytes) -> UnsubArg:
    """
    Parses arguments for the UNSUB command.

    Args:
        data (bytes): The raw buffer containing UNSUB command arguments.

    Returns:
        UnsubArg: A structured UnsubArg object containing parsed data.

    Raises:
        ValueError: If the input data does not match the expected format.
    """
    args = split_args(data)

    if len(args) < 1 or len(args) > 2:
        raise ValueError(f"Invalid UNSUB command arguments: {data}")

    unsub_arg = UnsubArg(
        sid=int(args[0].decode()),
        max_msgs=int(args[1].decode()) if len(args) == 2 else None
    )

    return unsub_arg

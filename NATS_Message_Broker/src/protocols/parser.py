from typing import Callable, Optional
from constants.state import State
from constants.kind import Kind
from constants.control_chars import ControlChars as cc
from messages.args import PubArg
from messages.message import Message
from utils.arg_parsers import prepare_pub


class Parser:
    """
    Parses raw byte streams according to the NATS protocol.

    Attributes:
        state (State): The current state of the parser.
        arg_start (int): The start index of the current argument in the buffer.
        drop (int): Number of bytes to skip when slicing buffers.
        arg_buf (Optional[bytes]): A buffer storing concatenated arguments.
        pub_arg (Optional[PubArg]): Stores arguments for PUB commands.
        msg_buf (Optional[bytes]): A buffer storing the message payload.
        cb (Callable[[Message], None]): Callback invoked when parsing completes a message.
    """

    def __init__(self, cb: Callable[[Message], None]):
        self.state: State = State.OP_START
        self.cb: Callable[[Message], None] = cb
        self.arg_start: int = 0
        self.drop: int = 0
        self.arg_buf: Optional[bytes] = None
        self.pub_arg: Optional[PubArg] = None
        self.msg_buf: Optional[bytes] = None

    def parse(self, buf: bytes):
        """
        Parses a given buffer byte by byte.

        Args:
            buf (bytes): The input buffer to parse.
        """
        self.arg_start = 0
        self.drop = 0

        i = 0
        while i < len(buf):
            b = buf[i]

            match self.state:
                case State.OP_START:
                    if b in {cc.UPPERCASE_C, cc.LOWERCASE_C}:
                        self.state = State.OP_C
                    elif b in {cc.UPPERCASE_P, cc.LOWERCASE_P}:
                        self.state = State.OP_P
                    elif b in {cc.UPPERCASE_S, cc.LOWERCASE_S}:
                        self.state = State.OP_S
                    elif b in {cc.UPPERCASE_U, cc.LOWERCASE_U}:
                        self.state = State.OP_U
                    else:
                        raise self.fail(buf[i:])

                case State.OP_C:
                    if b in {cc.UPPERCASE_O, cc.LOWERCASE_O}:
                        self.state = State.OP_CO
                    else:
                        raise self.fail(buf[i:])

                case State.OP_CO:
                    if b in {cc.UPPERCASE_N, cc.LOWERCASE_N}:
                        self.state = State.OP_CON
                    else:
                        raise self.fail(buf[i:])

                case State.OP_CON:
                    if b in {cc.UPPERCASE_N, cc.LOWERCASE_N}:
                        self.state = State.OP_CONN
                    else:
                        raise self.fail(buf[i:])

                case State.OP_CONN:
                    if b in {cc.UPPERCASE_E, cc.LOWERCASE_E}:
                        self.state = State.OP_CONNE
                    else:
                        raise self.fail(buf[i:])

                case State.OP_CONNE:
                    if b in {cc.UPPERCASE_C, cc.LOWERCASE_C}:
                        self.state = State.OP_CONNEC
                    else:
                        raise self.fail(buf[i:])

                case State.OP_CONNEC:
                    if b in {cc.UPPERCASE_T, cc.LOWERCASE_T}:
                        self.state = State.OP_CONNECT
                    else:
                        raise self.fail(buf[i:])

                case State.OP_CONNECT:
                    if b in {cc.SPACE, cc.TAB}:
                        pass
                    else:
                        self.state = State.CONNECT_ARG
                        self.arg_start = i

                case State.CONNECT_ARG:
                    if b == cc.CARRIAGE_RETURN:
                        self.drop = 1
                    elif b == cc.LINE_FEED:
                        self.process_arg(buf, i, Kind.CONNECT)
                        self.state = State.OP_START

                case State.OP_P:
                    if b in {cc.UPPERCASE_I, cc.LOWERCASE_I}:
                        self.state = State.OP_PI
                    elif b in {cc.UPPERCASE_O, cc.LOWERCASE_O}:
                        self.state = State.OP_PO
                    elif b in {cc.UPPERCASE_U, cc.LOWERCASE_U}:
                        self.state = State.OP_PU
                    else:
                        raise self.fail(buf[i:])

                case State.OP_PI:
                    if b in {cc.UPPERCASE_N, cc.LOWERCASE_N}:
                        self.state = State.OP_PIN
                    else:
                        raise self.fail(buf[i:])

                case State.OP_PIN:
                    if b in {cc.UPPERCASE_G, cc.LOWERCASE_G}:
                        self.state = State.OP_PING
                    else:
                        raise self.fail(buf[i:])

                case State.OP_PING:
                    if b == cc.LINE_FEED:
                        self.cb(Message(kind=Kind.PING))
                        self.state = State.OP_START

                case State.OP_PO:
                    if b in {cc.UPPERCASE_N, cc.LOWERCASE_N}:
                        self.state = State.OP_PON
                    else:
                        raise self.fail(buf[i:])

                case State.OP_PON:
                    if b in {cc.UPPERCASE_G, cc.LOWERCASE_G}:
                        self.state = State.OP_PONG
                    else:
                        raise self.fail(buf[i:])

                case State.OP_PONG:
                    if b == cc.LINE_FEED:
                        self.cb(Message(kind=Kind.PONG))
                        self.state = State.OP_START

                case State.OP_PU:
                    if b in {cc.UPPERCASE_B, cc.LOWERCASE_B}:
                        self.state = State.OP_PUB
                    else:
                        raise self.fail(buf[i:])

                case State.OP_PUB:
                    if b in {cc.SPACE, cc.TAB}:
                        pass
                    else:
                        self.state = State.PUB_ARG
                        self.arg_start = i

                case State.PUB_ARG:
                    if b == cc.CARRIAGE_RETURN:
                        self.drop = 1
                    elif b == cc.LINE_FEED:
                        arg = self.process_pub_arg(buf, i)
                        self.state = State.MSG_PAYLOAD
                        self.pub_arg = prepare_pub(arg)

                case State.MSG_PAYLOAD:
                    self.process_payload(buf, i)
                    self.state = State.MSG_END_CR

                case State.MSG_END_CR:
                    if b != cc.CARRIAGE_RETURN:
                        raise self.fail(buf[i:])
                    self.state = State.MSG_END_LF

                case State.MSG_END_LF:
                    if b != cc.LINE_FEED:
                        raise self.fail(buf[i:])
                    self.cb(Message(kind=Kind.PUB, pub_arg=self.pub_arg))
                    self.state = State.OP_START

                case _:
                    raise self.fail(buf[i:])
            i += 1

    def process_arg(self, buf: bytes, i: int, kind: Kind):
        """
        Processes a parsed argument and invokes the callback.
        """
        arg = buf[self.arg_start : i - self.drop]
        self.cb(Message(kind=kind, data=arg))

    def process_pub_arg(self, buf: bytes, i: int) -> bytes:
        """
        Processes the PUB command arguments.
        """
        if self.arg_buf is None:
            return buf[self.arg_start : i - self.drop]
        return self.arg_buf + buf[self.arg_start : i - self.drop]

    def process_payload(self, buf: bytes, i: int):
        """
        Processes the payload for PUB commands.
        """
        payload = buf[self.arg_start : i]
        self.msg_buf = payload if self.msg_buf is None else self.msg_buf + payload

    def fail(self, data: bytes) -> Exception:
        """
        Raises a parsing error.
        """
        return Exception(f"Parsing error at state {self.state}: {data}")

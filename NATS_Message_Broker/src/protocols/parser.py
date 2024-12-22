from typing import Callable, Optional
from src.constants import LEN_CRLF
from src.constants.state import State
from src.constants.kind import Kind
from src.constants.control_chars import ControlChars as cc
from src.messages.args import PubArg
from src.messages.message import Message
from src.utils.arg_parsers import prepare_pub


class Parser:
    def __init__(self, cb: Callable[[Message], None]):
        self.state: State = State.OP_START
        self.cb: Callable[[Message], None] = cb
        self.arg_start: int = 0
        self.drop: int = 0
        self.arg_buf: Optional[bytes] = None
        self.pub_arg: Optional[PubArg] = None
        self.msg_buf: Optional[bytes] = None

    def parse(self, buf: bytes):
        self.arg_start = 0
        self.drop = 0
        i = 0

        while i < len(buf):
            buffer = buf[i]

            match self.state:
                case State.OP_START:
                    match buffer:
                        case cc.UPPERCASE_C | cc.LOWERCASE_C:
                            self.state = State.OP_C
                        case cc.UPPERCASE_P | cc.LOWERCASE_P:
                            self.state = State.OP_P
                        case cc.UPPERCASE_S | cc.LOWERCASE_S:
                            self.state = State.OP_S
                        case cc.UPPERCASE_U | cc.LOWERCASE_U:
                            self.state = State.OP_U
                        case _:
                            raise self.fail(buf[i:])

                case State.OP_C:
                    match buffer:
                        case cc.UPPERCASE_O | cc.LOWERCASE_O:
                            self.state = State.OP_CO
                        case _:
                            raise self.fail(buf[i:])

                case State.OP_CO:
                    match buffer:
                        case cc.UPPERCASE_N | cc.LOWERCASE_N:
                            self.state = State.OP_CON
                        case _:
                            raise self.fail(buf[i:])

                case State.OP_CON:
                    match buffer:
                        case cc.UPPERCASE_N | cc.LOWERCASE_N:
                            self.state = State.OP_CONN
                        case _:
                            raise self.fail(buf[i:])

                case State.OP_CONN:
                    match buffer:
                        case cc.UPPERCASE_E | cc.LOWERCASE_E:
                            self.state = State.OP_CONNE
                        case _:
                            raise self.fail(buf[i:])

                case State.OP_CONNE:
                    match buffer:
                        case cc.UPPERCASE_C | cc.LOWERCASE_C:
                            self.state = State.OP_CONNEC
                        case _:
                            raise self.fail(buf[i:])

                case State.OP_CONNEC:
                    match buffer:
                        case cc.UPPERCASE_T | cc.LOWERCASE_T:
                            self.state = State.OP_CONNECT
                        case _:
                            raise self.fail(buf[i:])

                case State.OP_CONNECT:
                    match buffer:
                        case cc.TAB | cc.SPACE:
                            pass
                        case _:
                            self.state = State.CONNECT_ARG
                            self.arg_start = i

                case State.CONNECT_ARG:
                    
                    match buffer:
                        case cc.CARRIAGE_RETURN:
                            self.drop = 1
                        case cc.LINE_FEED:
                            if self.arg_buf:
                                arg = self.arg_buf + buf[self.arg_start:i - self.drop]
                                self.arg_buf = None
                            else:
                                arg = buf[self.arg_start:i - self.drop]
                            self.cb(Message(kind=Kind.CONNECT, data=arg))
                            self.arg_start = i + 1
                            self.drop = 0
                            self.state = State.OP_START
                        case _:
                            pass

                case State.OP_P:
                    match buffer:
                        case cc.UPPERCASE_I | cc.LOWERCASE_I:
                            self.state = State.OP_PI
                        case cc.UPPERCASE_O | cc.LOWERCASE_O:
                            self.state = State.OP_PO
                        case cc.UPPERCASE_U | cc.LOWERCASE_U:
                            self.state = State.OP_PU
                        case _:
                            raise self.fail(buf[i:])

                case State.OP_PI:
                    match buffer:
                        case cc.UPPERCASE_N | cc.LOWERCASE_N:
                            self.state = State.OP_PIN
                        case _:
                            raise self.fail(buf[i:])

                case State.OP_PIN:
                    match buffer:
                        case cc.UPPERCASE_G | cc.LOWERCASE_G:
                            self.state = State.OP_PING
                        case _:
                            raise self.fail(buf[i:])

                case State.OP_PING:
                    match buffer:
                        case cc.LINE_FEED:
                            self.cb(Message(kind=Kind.PING))
                            self.drop = 0
                            self.state = State.OP_START

                case State.OP_PO:
                    match buffer:
                        case cc.UPPERCASE_N | cc.LOWERCASE_N:
                            self.state = State.OP_PON
                        case _:
                            raise self.fail(buf[i:])

                case State.OP_PON:
                    match buffer:
                        case cc.UPPERCASE_G | cc.LOWERCASE_G:
                            self.state = State.OP_PONG
                        case _:
                            raise self.fail(buf[i:])

                case State.OP_PONG:
                    match buffer:
                        case cc.LINE_FEED:
                            self.cb(Message(kind=Kind.PONG))
                            self.drop = 0
                            self.state = State.OP_START

                case State.OP_S:
                    match buffer:
                        case cc.UPPERCASE_U | cc.LOWERCASE_U:
                            self.state = State.OP_SU
                        case _:
                            raise self.fail(buf[i:])

                case State.OP_SU:
                    match buffer:
                        case cc.UPPERCASE_B | cc.LOWERCASE_B:
                            self.state = State.OP_SUB
                        case _:
                            raise self.fail(buf[i:])

                case State.OP_SUB:
                    match buffer:
                        case cc.SPACE | cc.TAB:
                            pass
                        case _:
                            self.state = State.SUB_ARG
                            self.arg_start = i

                case State.SUB_ARG:
                    match buffer:
                        case cc.CARRIAGE_RETURN:
                            self.drop = 1
                        case cc.LINE_FEED:
                            if self.arg_buf:
                                arg = self.arg_buf + \
                                    buf[self.arg_start:i -
                                        self.drop]
                                self.arg_buf = None
                            else:
                                arg = buf[self.arg_start:i - self.drop]

                            self.cb(Message(kind=Kind.SUB, data=arg))
                            self.arg_start = i + 1
                            self.drop = 0
                            self.state = State.OP_START
                        case _:
                            pass

                case State.OP_PU:
                    match buffer:
                        case cc.UPPERCASE_B | cc.LOWERCASE_B:
                            self.state = State.OP_PUB
                        case _:
                            raise self.fail(buf[i:])

                case State.OP_PUB:
                    match buffer:
                        case cc.SPACE | cc.TAB:
                            pass
                        case _:
                            self.state = State.PUB_ARG
                            self.arg_start = i

                case State.PUB_ARG:
                    match buffer:
                        case cc.CARRIAGE_RETURN:
                            self.drop = 1
                        case cc.LINE_FEED:
                            arg = self.arg_buf + \
                                buf[self.arg_start:i -
                                    self.drop] if self.arg_buf else buf[self.arg_start:i - self.drop]
                            self.pub_arg = prepare_pub(arg)
                            
                            if self.pub_arg.payload_size <= 0:
                                raise Exception("Parsing error: Invalid PUB payload size")
                            
                            self.arg_start = i + 1
                            self.drop = 0
                            self.state = State.MSG_PAYLOAD

                            if self.msg_buf is None:
                                i = self.arg_start + self.pub_arg.payload_size - LEN_CRLF

                        case _:
                            pass

                case State.MSG_PAYLOAD:
                    if self.msg_buf:
                        if self.pub_arg and i + len(self.msg_buf) + 1 >= self.pub_arg.payload_size:
                            self.state = State.MSG_END_CR
                        else:
                            pass

                    elif self.pub_arg and i - self.arg_start + 1 >= self.pub_arg.payload_size:
                        if i - self.arg_start + 1 < self.pub_arg.payload_size:
                            raise Exception(f"Parsing error: Incomplete PUB payload, expected {self.pub_arg.payload_size} bytes")
                        self.state = State.MSG_END_CR

                case State.MSG_END_CR:
                    match buffer:
                        case cc.CARRIAGE_RETURN:
                            self.drop = 1
                            self.state = State.MSG_END_LF
                        case _:
                            raise self.fail(buf[self.arg_start:])

                case State.MSG_END_LF:
                    match buffer:
                        case cc.LINE_FEED:
                            if self.msg_buf is None:
                                self.pub_arg.payload = buf[self.arg_start:i - self.drop]
                            else:
                                self.pub_arg.payload = self.msg_buf + \
                                    buf[self.arg_start:i - self.drop]

                            self.cb(Message(kind=Kind.PUB, pub_arg=self.pub_arg))
                            self.arg_buf = None
                            self.msg_buf = None
                            self.arg_start = i + 1
                            self.drop = 0
                            self.state = State.OP_START
                        case _:
                            raise self.fail(buf[self.arg_start:])

                case State.OP_U:
                    match buffer:
                        case cc.UPPERCASE_N | cc.LOWERCASE_N:
                            self.state = State.OP_UN
                        case _:
                            raise self.fail(buf[i:])

                case State.OP_UN:
                    match buffer:
                        case cc.UPPERCASE_S | cc.LOWERCASE_S:
                            self.state = State.OP_UNS
                        case _:
                            raise self.fail(buf[i:])

                case State.OP_UNS:
                    match buffer:
                        case cc.UPPERCASE_U | cc.LOWERCASE_U:
                            self.state = State.OP_UNSU
                        case _:
                            raise self.fail(buf[i:])

                case State.OP_UNSU:
                    match buffer:
                        case cc.UPPERCASE_B | cc.LOWERCASE_B:
                            self.state = State.OP_UNSUB
                        case _:
                            raise self.fail(buf[i:])

                case State.OP_UNSUB:
                    match buffer:
                        case cc.SPACE | cc.TAB:
                            pass
                        case _:
                            self.state = State.UNSUB_ARG
                            self.arg_start = i

                case State.UNSUB_ARG:
                    match buffer:
                        case cc.CARRIAGE_RETURN:
                            self.drop = 1
                        case cc.LINE_FEED:
                            if (self.arg_buf):
                                arg = self.arg_buf + \
                                    buf[self.arg_start:i -
                                        self.drop]
                                self.arg_buf = None
                            else:
                                arg = buf[self.arg_start:i - self.drop]
                            self.cb(Message(kind=Kind.UNSUB, data=arg))
                            self.arg_start = i + 1
                            self.drop = 0
                            self.state = State.OP_START
                        case _:
                            pass
                
                case _:
                    raise Exception(f"Parsing error: Invalid state {self.state}")

            i += 1

        if self.state in {State.CONNECT_ARG, State.SUB_ARG, State.PUB_ARG, State.UNSUB_ARG}:
            if self.arg_buf is None:
                self.arg_buf = buf[self.arg_start:i - self.drop]
            else:
                self.arg_buf += buf[self.arg_start:i - self.drop]

        if self.state in {State.MSG_PAYLOAD, State.MSG_END_CR, State.MSG_END_LF}:
            if self.msg_buf is None:
                self.msg_buf = buf[self.arg_start:i - self.drop]
            else:
                self.msg_buf += buf[self.arg_start:i - self.drop]

            if self.arg_buf is None:
                self.clone_pub_arg()

    def clone_pub_arg(self):
        """
        Allocates a new buffer to store the subject and reply_to arguments
        and updates self.pub_arg with the newly allocated memory.

        This ensures the buffers are independent of the original memory reference.
        """
        if self.pub_arg is None:
            raise ValueError("pub_arg is None while attempting to clone it")

        subject_length = len(self.pub_arg.subject)
        reply_to_length = len(
            self.pub_arg.reply_to) if self.pub_arg.reply_to else 0

        new_buf = bytearray(subject_length + reply_to_length)

        new_buf[:subject_length] = self.pub_arg.subject
        if self.pub_arg.reply_to:
            new_buf[subject_length:] = self.pub_arg.reply_to

        self.arg_buf = new_buf

        self.pub_arg.subject = new_buf[:subject_length]
        if self.pub_arg.reply_to:
            self.pub_arg.reply_to = new_buf[subject_length:]

    def fail(self, data: bytes) -> Exception:
        """
        Raises a parsing error.
        """
        return Exception(f"Parsing error at state {self.state}: {data}")

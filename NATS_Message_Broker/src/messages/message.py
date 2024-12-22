from typing import Optional
from src.constants.kind import Kind
from src.messages.args import PubArg, SubArg, UnsubArg


class Message:
    """
    Represents a NATS protocol message.

    Attributes:
        kind (Kind): The type of message (e.g., CONNECT, PING, PUB).
        data (Optional[bytes]): Any associated data for the message.
        pub_arg (Optional[PubArg]): Arguments for the PUB command, if applicable.
    """

    def __init__(
        self,
        kind: Kind,
        data: Optional[bytes] = None,
        pub_arg: Optional[PubArg] = None,
    ):
        """
        Initializes a new Message object.

        Args:
            kind (Kind): The type of message being processed.
            data (Optional[bytes]): The payload or data associated with the message.
            pub_arg (Optional[PubArg]): Arguments specific to the PUB command.
        """
        self.kind: Kind = kind
        self.data: Optional[bytes] = data
        self.pub_arg: Optional[PubArg] = pub_arg

    def __eq__(self, other):
        """
        Determines equality based on attribute values.

        Args:
            other (Message): The other Message object to compare.

        Returns:
            bool: True if the messages have the same attributes, otherwise False.
        """
        if not isinstance(other, Message):
            return False
        return (
            self.kind == other.kind
            and self.data == other.data
            and self.pub_arg == other.pub_arg
        )

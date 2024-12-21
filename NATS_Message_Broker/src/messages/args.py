from typing import Optional
from dataclasses import dataclass

@dataclass
class SubArg:
    """
    Represents the arguments passed with the SUB command.

    Attributes:
        subject (bytes): The subject to subscribe to.
        group (Optional[bytes]): The optional group for the subscription.
        sid (int): The subscription ID.
    """
    subject: bytes
    group: Optional[bytes] = None
    sid: int


@dataclass
class PubArg:
    """
    Represents the arguments passed with the PUB command.

    Attributes:
        subject (bytes): The subject to publish to.
        reply_to (Optional[bytes]): The optional reply-to subject.
        payload_size (int): The size of the message payload.
        payload (Optional[bytes]): The actual message payload.
    """
    subject: bytes
    reply_to: Optional[bytes] = None
    payload_size: int
    payload: Optional[bytes] = None


@dataclass
class UnsubArg:
    """
    Represents the arguments passed with the UNSUB command.

    Attributes:
        sid (int): The subscription ID to unsubscribe from.
        max_msgs (Optional[int]): The optional maximum number of messages to receive before unsubscribing.
    """
    sid: int
    max_msgs: Optional[int] = None

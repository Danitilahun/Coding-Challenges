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
    sid: int
    group: Optional[bytes] = None

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
    payload_size: int
    reply_to: Optional[bytes] = None
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
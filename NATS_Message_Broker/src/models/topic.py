from typing import Set, Optional
from messages.args import PubArg
from subscription import Subscription
import asyncio

class Topic:
    """
    Represents a topic for managing SUB, UNSUB, and PUB commands.

    Attributes:
        subject (str): The subject of the topic.
        subscriptions (Set[Subscription]): A set of subscriptions for this topic.
    """

    def __init__(self, subject: str, subscriptions: Optional[Set[Subscription]] = None):
        """
        Initialize a Topic instance.

        Args:
            subject (str): The subject of the topic.
            subscriptions (Optional[Set[Subscription]]): Optional set of subscriptions.
        """
        self._subject = subject
        self._subscriptions = subscriptions or set()

    def sub(self, subscription: Subscription):
        """
        Adds the given subscription to this topic.

        Args:
            subscription (Subscription): The subscription to add.
        """
        self._subscriptions.add(subscription)

    def unsub(self, subscription: Subscription):
        """
        Removes the given subscription from this topic.

        Args:
            subscription (Subscription): The subscription to remove.
        """
        self._subscriptions.discard(subscription)

    async def publish(self, pub_arg: PubArg):
        """
        Publishes the message to all subscribed clients.

        Args:
            pub_arg (PubArg): The arguments for publishing the message.

        Returns:
            None
        """
        prefix = f"MSG {self._subject} ".encode()
        suffix = (
            f"{pub_arg.payload_size}\r\n".encode() + pub_arg.payload + b"\r\n"
            if pub_arg.payload
            else b"0\r\n\r\n"
        )

        tasks = []
        for subscription in self._subscriptions:
            buffer = (
                prefix + f"{subscription.sid} ".encode() + suffix
            )
            tasks.append(asyncio.to_thread(subscription.client.connection.sendall, buffer))

        await asyncio.gather(*tasks)

from dataclasses import dataclass
from client import Client

@dataclass
class Subscription:
    """
    Represents a subscription to a specific subject in the server.

    Attributes:
        client (Client): The client associated with this subscription.
        sid (int): The unique alphanumeric subscription ID of the subject.
        subject (str): The subject name.
    """
    client: Client
    sid: int
    subject: str

    def __init__(self, client: Client, sid: int, subject: str):
        self.client = client
        self.sid = sid
        self.subject = subject
import socket
from src.models.client_options import ClientOptions
from src.models.default_options import DEFAULT_OPTIONS

class Client:
    def __init__(self, key: str, connection: socket.socket, options: ClientOptions = DEFAULT_OPTIONS):
        """
        Initialize the client with a unique key, socket connection, and options.
        """
        self.key = key
        self.connection = connection
        self.options = options

    def update_options(self, data: dict):
        """
        Update the client's options by merging with new data.
        """
        for key, value in data.items():
            if hasattr(self.options, key):
                setattr(self.options, key, value)

    def send_pong(self):
        """
        Send a PONG message to the client.
        """
        self.connection.sendall(b"PONG\r\n")

    def send_ok(self):
        """
        Send an OK message if the verbose option is enabled.
        """
        if self.options.verbose:
            self.connection.sendall(b"+OK\r\n")

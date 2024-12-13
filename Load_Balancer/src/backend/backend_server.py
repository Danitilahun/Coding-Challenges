import socket
import threading


class BackendServer:
    """
    Represents a backend server in a load-balanced system. Handles client connections
    and forwards data between the client and the backend server.
    """

    def __init__(self, server_id: int, host: str, port: int) -> None:
        """
        Initialize the backend server with its ID, host, and port.

        Args:
            server_id (int): Unique identifier for the backend server.
            host (str): The hostname or IP address of the backend server.
            port (int): The port number of the backend server.
        """
        self.server_id: int = server_id
        self.host: str = host
        self.port: int = port
        self.is_up: bool = True
        self.lock: threading.Lock = threading.Lock()
        self.active_connections: int = 0

    def connect(self) -> socket.socket:
        """
        Establish a connection to the backend server.

        Returns:
            socket.socket: The socket connected to the backend server.
        """
        backend_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        backend_connection.connect((self.host, self.port))
        return backend_connection

    def handle_connection(self, client_connection: socket.socket) -> None:
        """
        Manage the connection between a client and the backend server. 
        Creates threads to forward data in both directions.

        Args:
            client_connection (socket.socket): The socket representing the client connection.
        """
        def forward_data(source: socket.socket, destination: socket.socket) -> None:
            """
            Forward data from the source socket to the destination socket.

            Args:
                source (socket.socket): The socket to read data from.
                destination (socket.socket): The socket to write data to.
            """
            with self.lock:
                self.active_connections += 1
            try:
                while True:
                    data = source.recv(1024)
                    if not data:
                        break
                    destination.send(data)
            finally:
                with self.lock:
                    self.active_connections -= 1

        backend_connection = self.connect()

        # Create threads for bidirectional communication
        client_to_backend = threading.Thread(target=forward_data, args=(client_connection, backend_connection))
        backend_to_client = threading.Thread(target=forward_data, args=(backend_connection, client_connection))

        # Start threads
        client_to_backend.start()
        backend_to_client.start()

        # Wait for threads to complete
        client_to_backend.join()
        backend_to_client.join()

        # Close the connections
        client_connection.close()
        backend_connection.close()

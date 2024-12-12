import socket
import threading


class BackendServer:
    """
    A class representing a backend server that handles client requests.

    Attributes:
        id (int): The unique identifier for the backend server.
        host (str): The host IP address of the backend server.
        port (int): The port number on which the backend server is listening.
        is_up (bool): A flag indicating whether the backend server is currently up.
        lock (threading.Lock): A lock used to manage concurrent access to shared resources.
        num_connections (int): The number of active connections the server is handling.
        backend_connection (socket.socket): The socket connection to the backend server.

    Methods:
        connect(): Establishes a connection to the backend server.
        handle_client_request(client_conn): Handles data forwarding between the client and the backend server.
    """

    def __init__(self, id: int, host: str, port: int) -> None:
        """
        Initializes the BackendServer instance.

        Args:
            id (int): The unique identifier for the backend server.
            host (str): The host IP address of the backend server.
            port (int): The port number the backend server will use to accept connections.
        """
        self.id = id
        self.host = host
        self.port = port
        self.is_up = True
        self.lock = threading.Lock()
        self.num_connections = 0

    def connect(self) -> None:
        """
        Establishes a connection to the backend server using the provided host and port.
        """
        self.backend_connection = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        self.backend_connection.connect((self.host, self.port))

    def handle_client_request(self, client_conn: socket.socket) -> None:
        """
        Handles data forwarding between the client and the backend server.

        Args:
            client_conn (socket.socket): The connection from the client to the load balancer.

        This method starts two threads:
            - One to forward data from the client to the backend server.
            - Another to forward data from the backend server to the client.
        """
        def forward_request(source: socket.socket, dest: socket.socket) -> None:
            """
            Forwards data from the source socket to the destination socket.

            Args:
                source (socket.socket): The source socket to read data from.
                dest (socket.socket): The destination socket to send data to.
            """
            print(f"[Backend Server]: Sending data from {
                  source.getsockname()} to {dest.getsockname()}...")

            with self.lock:
                self.num_connections += 1

            try:
                while True:
                    data = source.recv(1024)
                    if len(data) == 0:
                        break
                    dest.send(data)
            finally:
                with self.lock:
                    self.num_connections -= 1

        self.connect()

        # Start threads for forwarding data
        client_to_backend = threading.Thread(
            target=forward_request, args=(client_conn, self.backend_connection))
        backend_to_client = threading.Thread(
            target=forward_request, args=(self.backend_connection, client_conn))

        # Start thread execution
        client_to_backend.start()
        backend_to_client.start()

        # Wait for the threads to complete
        client_to_backend.join()
        backend_to_client.join()

        # Close the connections
        client_conn.close()
        self.backend_connection.close()

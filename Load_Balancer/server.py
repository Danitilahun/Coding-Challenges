import socket
import sys
from time import sleep
import argparse


class SimpleHTTPServer:
    """
    A simple HTTP server that listens for incoming TCP connections
    and responds with a predefined HTTP message. It is designed to
    simulate a basic backend service.
    """

    def __init__(self, host: str, port: int):
        """
        Initialize the server with a host and port.

        Args:
            host (str): The hostname or IP address the server binds to.
            port (int): The port number on which the server listens for incoming connections.
        """
        self.host = host
        self.port = port

    def start(self):
        """
        Start the server to listen for incoming connections. This is a blocking call
        that will keep the server running indefinitely, processing one connection
        at a time.

        The server listens on the specified host and port, and accepts incoming
        connections in a loop.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            try:
               
                server_socket.bind((self.host, self.port))
                
                # Start listening for incoming connections (maximum of 5 queued connections)
                server_socket.listen(5)
                
                print(f"[Server]: Listening on {self.host}:{self.port}...")

                
                while True:
                    client_connection, client_address = server_socket.accept()
                    self._handle_connection(client_connection, client_address)

            except Exception as error:
                print(f"[Server]: Error occurred: {error}")
           
    def _handle_connection(self, client_connection, client_address):
        """
        Handle an individual client connection. Receives data from the client,
        processes it, and sends back an HTTP response.

        Args:
            client_connection (socket): The socket object representing the client connection.
            client_address (tuple): The address (IP and port) of the connected client.
        """
        with client_connection:
            print(f"[Server]: Connected to {client_address}")
            try:
                
                request_data = client_connection.recv(1024).decode('utf-8')
                if not request_data:
                    # If no data is received, terminate handling for this connection
                    return

                print(f"[Server]: Received data from {client_address}")

              
                response_body = f"[Server]: Hello from Backend Server ({self.host}:{self.port})"
                http_response = (
                    f"HTTP/1.1 200 OK\r\n"
                    f"Content-Length: {len(response_body)}\r\n"
                    f"\r\n"
                    f"{response_body}"
                )

                
                sleep(10)

                client_connection.send(http_response.encode())

            except Exception as error:
                print(f"[Server]: Error handling connection: {error}")
           


def parse_arguments():
    """
    Parse command-line arguments to configure the server.

    Returns:
        argparse.Namespace: Parsed arguments containing the host and port for the server.
    """
    parser = argparse.ArgumentParser(description="Run a simple HTTP server.")
    parser.add_argument(
        "--host", type=str, default="localhost",
        help="The hostname or IP address to bind to (default: localhost)."
    )
    parser.add_argument(
        "--port", type=int, default=5001,
        help="The port number to listen on (default: 5001)."
    )
    return parser.parse_args()


if __name__ == "__main__":
   
    args = parse_arguments()

    server = SimpleHTTPServer(host=args.host, port=args.port)

    server.start()

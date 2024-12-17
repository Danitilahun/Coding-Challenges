"""
This module implements a Redis-like TCP server that listens for client connections, 
processes requests using RESP (Redis Serialization Protocol), and sends back 
serialized responses.

The server handles multiple clients concurrently using threading.

Modules:
    - arg_parser: Parses server host and port arguments.
    - request_handler: Processes RESP-encoded requests and generates responses.
"""

import logging
import socket
import threading

from src.handlers.request_handler import process_request
from src.utils.argument_parser import parse_arguments

logger = logging.getLogger(__name__)

args = parse_arguments()
HOST = args.host
PORT = args.port


def handle_client(connection):
    """
    Handles communication with a single client.

    Args:
        connection (socket): The socket connection to the client.

    This function continuously listens for data, processes it, and sends back responses.
    """
    with connection:
        while True:
            try:
                data = connection.recv(1024)
                if not data:
                    break

                response = process_request(data)
                connection.sendall(response)

            except Exception as e:
                logger.exception("Error while handling client: %s", e)
                break


def start_server():
    """
    Starts the Redis-like server to listen for incoming client connections.

    - Binds the server to the specified HOST and PORT.
    - Accepts incoming client connections and handles them in separate threads.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as lsock:
        try:

            lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            lsock.bind((HOST, PORT))
            lsock.listen()

            logger.info(f"Server started. Listening on {HOST}:{PORT}...")

            while True:
                client_socket, address = lsock.accept()
                logger.info(f"New connection from {address}")

                client_handler = threading.Thread(
                    target=handle_client, args=(client_socket,)
                )
                client_handler.start()

        except KeyboardInterrupt:
            logger.info("Server stopped by user.")
        except Exception as e:
            logger.exception("An error occurred: %s", e)


if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    start_server()


import argparse

from simple_http_server.simple_http_server import SimpleHTTPServer

def parse_arguments() -> argparse.Namespace:
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
    args: argparse.Namespace = parse_arguments()
    server: SimpleHTTPServer = SimpleHTTPServer(host=args.host, port=args.port)
    server.start()

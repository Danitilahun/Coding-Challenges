"""
This module provides a utility function to parse command-line arguments
for configuring the Redis server's host and port.

Usage:
    Place this module in the 'utils' directory and import the `parse_arguments` function
    wherever argument parsing is required.

Features:
- Default values for host and port (127.0.0.1, 65432).
- Customizable descriptions and help text.
- Easy-to-extend structure for additional arguments.
"""

import argparse


def parse_arguments(default_host: str = "127.0.0.1", default_port: int = 65432):
    """
    Parses command-line arguments for configuring the Redis server.

    Args:
        default_host (str): Default host address. Defaults to '127.0.0.1'.
        default_port (int): Default port number. Defaults to 65432.

    Returns:
        argparse.Namespace: Parsed command-line arguments.
    
    Example:
        Run the program with:
        python main.py --host 192.168.0.1 --port 8080
    """
    parser = argparse.ArgumentParser(
        prog="Redis Server",
        description="A lightweight Redis-like server supporting host and port configuration."
    )

    parser.add_argument(
        "--host",
        "-H",
        type=str,
        default=default_host,
        metavar="HOST",
        help=f"Host address to bind the server. Defaults to '{default_host}'."
    )

    parser.add_argument(
        "--port",
        "-p",
        type=int,
        default=default_port,
        metavar="PORT",
        help=f"Port number to run the server. Defaults to '{default_port}'."
    )

    parser.add_argument(
        "--snapshot",
        "-s",
        type=str,
        default="redis_snapshot.pkl",
        metavar="SNAPSHOT_FILE",
        help="Path to the snapshot file for persistence. Defaults to 'redis_snapshot.pkl'."
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose mode for detailed logging."
    )

    return parser.parse_args()
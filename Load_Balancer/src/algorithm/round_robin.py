from typing import List

from src.backend.backend_server import BackendServer

class RoundRobin:
    """
    Implements the Round Robin algorithm for load balancing, distributing requests
    across a list of backend servers in a circular order.
    """

    def __init__(self, servers: List[BackendServer]) -> None:
        """
        Initialize the Round Robin load balancing algorithm with a list of servers.

        Args:
            servers (List[BackendServer]): A list of backend server instances to balance requests across.
        """
        self.servers: List[BackendServer] = servers
        self.current_index: int = 0

    def get_next_server(self) -> BackendServer:
        """
        Retrieve the next available server using the Round Robin algorithm. Skips
        servers that are marked as down.

        Returns:
            BackendServer: The next available server instance.

        Raises:
            ValueError: If no servers are available or all servers are down.
        """
        if not self.servers:
            raise ValueError("[ERROR]: No available servers...")

        original_index = self.current_index

        while True:
            next_server = self.servers[self.current_index]
            self.current_index = (self.current_index + 1) % len(self.servers)

            if next_server.is_up:
                return next_server

            if self.current_index == original_index:
                raise ValueError("[ERROR]: No active servers available...")

from typing import List

from src.server.backend_server import BackendServer

class RoundRobin:
    """
    A class to implement the Round Robin load balancing algorithm.

    Attributes:
        servers (List[BackendServer]): List of backend server objects that the load balancer distributes requests to.
        current_index (int): Index of the next server to send the request to.
    
    Methods:
        get_next_server(): Selects the next available backend server based on the round robin strategy.
    """

    def __init__(self, servers: List[BackendServer]) -> None:
        """
        Initializes the RoundRobin load balancer with the list of backend servers.

        Args:
            servers (List[BackendServer]): List of backend server objects that the load balancer will manage.
        """
        self.servers: List[BackendServer] = servers
        self.current_index: int = 0

    def get_next_server(self) -> BackendServer:
        """
        Returns the next available backend server using the round robin method.

        Loops through the backend servers and returns the next one that is up (i.e., is_active). 
        If no server is available, raises a ValueError.

        Returns:
            BackendServer: The next available backend server.

        Raises:
            ValueError: If no servers are available or all servers are down.
        """
        if not self.servers:
            raise ValueError("[ERROR]: No available servers...")

        original_index: int = self.current_index

        while True:
            next_server: BackendServer = self.servers[self.current_index]
            self.current_index = (self.current_index + 1) % len(self.servers)

            # Return the first server that is up
            if next_server.is_up:
                return next_server

            # If we've cycled through all servers and none are up, raise an error
            if self.current_index == original_index:
                raise ValueError("[ERROR]: No active servers available...")

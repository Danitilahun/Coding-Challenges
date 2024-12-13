import socket
from threading import Thread
from typing import List
from algorithm.round_robin import RoundRobin
from backend.backend_server import BackendServer
from healthcheck.health_check import Healthcheck, start_health_check
from server_db.server_db import server_info


class LoadBalancer:
    """
    A Load Balancer that distributes incoming requests to backend servers using a specified algorithm.
    Supports health checks to monitor server availability.
    """

    def __init__(self, host: str, port: int, health_check_interval: int = 15) -> None:
        """
        Initialize the Load Balancer with the specified configuration.

        Args:
            host (str): The hostname or IP address for the load balancer.
            port (int): The port number the load balancer listens on.
            health_check_interval (int): Interval (in seconds) for health checks on backend servers.
        """
        self.host: str = host
        self.port: int = port
        self.health_check_interval: int = health_check_interval
        self.servers: List[BackendServer] = self._initialize_servers()
        self.load_balancing_algorithm: RoundRobin = RoundRobin(self.servers)
        self.health_check_threads: List[Thread] = []
        self.load_balancer_threads: List[Thread] = []

    def _initialize_servers(self) -> List[BackendServer]:
        """
        Initialize backend servers from the server database.

        Returns:
            List[Beserver]: A list of backend server instances.
        """
        servers: List[BackendServer] = []
        for server_data in server_info["server_list"]:
            servers.append(BackendServer(
                int(server_data["id"]),
                server_data["host"],
                int(server_data["port"])
            ))
        return servers

    def start(self) -> None:
        """
        Start the Load Balancer, listen for incoming client connections, and distribute them to backend servers.
        """
        self._start_health_checks()
        self._start_server()

    def _start_health_checks(self) -> None:
        """
        Start periodic health checks on backend servers.
        """
        health_checkers: List[Healthcheck] = [
            Healthcheck(server, self.health_check_interval) for server in self.servers
        ]
        self.health_check_threads = start_health_check(health_checkers)

    def _start_server(self) -> None:
        """
        Start the load balancer's main server loop to handle incoming client connections.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            try:
                server_socket.bind((self.host, self.port))
                server_socket.listen(100)
                print(f"[LoadBalancer]: Listening on {self.host}:{self.port}...")

                while True:
                    client_connection, client_address = server_socket.accept()
                    print(f"[LoadBalancer]: Connected by {client_address}")

                    backend_server: BackendServer = self.load_balancing_algorithm.get_next_server()

                    if backend_server and backend_server.is_up:
                        thread: Thread = Thread(target=backend_server.handle_connection, args=(client_connection,))
                        self.load_balancer_threads.append(thread)
                        thread.start()

            except Exception as error:
                print(f"[LoadBalancer]: Error occurred: {error}")

            except KeyboardInterrupt:
                print("Load Balancer interrupted by user (Ctrl-C).")

            finally:
                self._cleanup()

    def _cleanup(self) -> None:
        """
        Clean up resources by closing threads and ensuring all operations terminate gracefully.
        """
        for thread in self.load_balancer_threads:
            thread.join()

        for thread in self.health_check_threads:
            thread.join()
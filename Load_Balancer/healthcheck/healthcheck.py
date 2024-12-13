from typing import List
import requests
import time
from threading import Thread


class Healthcheck:
    """
    Performs periodic health checks on a backend server to monitor its availability.
    """

    def __init__(self, server, check_period: int) -> None:
        """
        Initialize the Healthcheck instance.

        Args:
            server: The server instance to monitor.
            check_period (int): The interval (in seconds) between health checks.
        """
        self.server = server
        self.check_period: int = check_period
        self.health_check_url: str = f"http://{self.server.host}:{self.server.port}/health"
        self.is_healthy: bool = True

    def health_check(self) -> None:
        """
        Continuously monitor the server's health status by sending HTTP GET requests
        to the server's health endpoint. Updates the server's availability status
        based on the response.
        """
        while True:
            try:
                response = requests.get(self.health_check_url)
                if response.status_code == 200:
                    if not self.is_healthy:
                        print(f"[Healthcheck]: Server {self.server.id} is now healthy. Adding it back to available servers.")
                        self.server.is_up = True
                        self.is_healthy = True
                else:
                   
                    if self.is_healthy:
                        print(f"[Healthcheck]: Server {self.server.id} returned status {response.status_code}. Marking it as unhealthy.")
                        self.server.is_up = False
                        self.is_healthy = False
            except requests.ConnectionError:
               
                if self.is_healthy:
                    print(f"[Healthcheck]: Server {self.server.id} is not reachable. Marking it as down.")
                    self.server.is_up = False
                    self.is_healthy = False
            except Exception as error:
               
                print(f"[Healthcheck]: Unexpected error during health check for server {self.server.id}: {error}")
                self.server.is_up = False
                self.is_healthy = False

            time.sleep(self.check_period)


def start_health_check(health_checkers: List[Healthcheck]) -> List[Thread]:
    """
    Start health checks for a list of Healthcheck instances.

    Args:
        health_checkers (List[Healthcheck]): A list of Healthcheck instances to monitor servers.

    Returns:
        List[Thread]: A list of threads running the health checks.
    """
    health_check_threads: List[Thread] = []

    for health_checker in health_checkers:
        health_check_thread = Thread(target=health_checker.health_check)
        health_check_thread.start()
        health_check_threads.append(health_check_thread)

    return health_check_threads

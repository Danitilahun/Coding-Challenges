from typing import List
import requests
import time
from threading import Thread

class Healthcheck:
    def __init__(self, server, check_period):
        self.server = server
        self.check_period = check_period
        self.health_check_url = f"http://{self.server.host}:{self.server.port}/health"
        self.is_healthy = True


    def health_check(self):
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
                        print(f"[Healthcheck]: Server {self.server.id} is not healthy. Removing it from available servers.")
                        self.server.is_up = False
                        self.is_healthy = False
                        
            except Exception:
                print(f"[Healthcheck]: Error during health check for server {self.server.id}...")
                self.server.is_up = False
                self.is_healthy = False
            
            time.sleep(self.check_period)


def start_health_check(health_checkers: List[Healthcheck]):
    health_check_threads = []

    for health_checker in health_checkers:
        health_check_thread = Thread(target=health_checker.health_check)
        health_check_thread.start()
        health_check_threads.append(health_check_thread)

    return health_check_threads

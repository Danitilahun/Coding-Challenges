import socket
import sys
from threading import Thread
from typing import List, Tuple
from backend.Beserver import Beserver
from algorithm.roundrobin import RoundRobin
from healthcheck.healthcheck import Healthcheck, start_health_check
from server_db.server_db import server_info


HOST: str = 'localhost'
if len(sys.argv) <= 1:
    PORT = 5432
else:
    PORT = int(sys.argv[1])

server_db = server_info["server_list"]
servers: List[Beserver] = []
for server in server_db:
    servers.append(Beserver(int(server["id"]),
                            server["host"],
                            int(server["port"])))

lb_algorithm = None

health_check_period = 15


def main():

    lb_algorithm = RoundRobin(servers)

    lb_threads: List[Thread] = []

    health_checkers = [Healthcheck(server, health_check_period)
                       for server in servers]

    health_check_threads = start_health_check(health_checkers)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:

        sock.bind((HOST, PORT))

        sock.listen(100)

        print(f"[LB]: Listening on port {PORT}...")

        while True:

            client_conn, client_addr = sock.accept()
            print(f"[LB]: Connected by {client_addr}...")

            be: Beserver = lb_algorithm.get_next_server()

            if be and be.is_up:

                lb_thread = Thread(
                    target=be.handle_beservers, args=(client_conn,))
                lb_threads.append(lb_thread)
                lb_thread.start()

    except Exception as e:
        print(f"Error handling connection: {e}")

    except KeyboardInterrupt:
        print("Ctrl-C pressed")

    finally:
        sock.close()
        map(lambda th: th.join(), lb_threads)

        for thread in health_check_threads:
            thread.join()


if __name__ == "__main__":
    main()

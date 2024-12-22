import sys

from src.server.nats_server import NATSServer

PORT = 4222
HOST = None
DEBUG = False

for arg in sys.argv[1:]:
    if arg == "--debug":
        DEBUG = True

server = NATSServer(port=PORT, host=HOST or "0.0.0.0", debug=DEBUG)

if __name__ == "__main__":
    try:
        server.start_server()
    except KeyboardInterrupt:
        print("Shutting down the server...")
        server.stop_server()

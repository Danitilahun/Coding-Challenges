import socket
import sys
from time import sleep

HOST = 'localhost'
if len(sys.argv) <= 1:
    PORT = 5001
else:
    PORT = int(sys.argv[1])

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:

            sock.bind((HOST, PORT))

            sock.listen(5)

            print(f"[S]: Server listening on port {PORT}...")

            while True:

                client_conn, client_addr = sock.accept()

                handle_connection(client_conn, client_addr)

        except Exception as e:
            print(f"[S]: Error handling connection: {e}")

        finally:
            sock.close()


def handle_connection(client_conn, client_addr):
    with client_conn:
        print(f"[S]: Connected by {client_addr}...")
        try:
           
            data = client_conn.recv(1024).decode('utf-8')
            if not data:
                return
            print(f"[S]: Received data from {client_conn.getpeername()}...")

            response = f"[S]: Hello from Backend Server: ({HOST}:{PORT})"
            http_response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(response)}\r\n\r\n{
                response}"
            sleep(10)

            client_conn.send(http_response.encode())

        except Exception as e:
            print(f"Error handling connection: {e}")


if __name__ == "__main__":
    start_server()

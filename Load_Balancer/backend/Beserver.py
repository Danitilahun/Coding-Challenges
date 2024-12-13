import socket
import threading

class Beserver:
    def __init__(self, id, host, port) -> None:
        self.id = id
        self.host = host 
        self.port = port
        self.is_up = True
        self.lock = threading.Lock()
        self.num_connections = 0
        
        
    def connect(self):
        self.be_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.be_conn.connect((self.host, self.port))
      

    def handle_beservers(self, client_conn):
        def forward_request(source, dest):
            
            print(f"[BE]: Sending data from {source.getsockname()} to {dest.getsockname()}...")
            
            with self.lock:
                    self.num_connections += 1
            try:
                while True:
                    data = source.recv(1024)
                    if len(data) == 0:
                        break
                    dest.send(data)
            finally:
                with self.lock:
                    self.num_connections -= 1
        
        # Backend socket connection
        self.connect()
        
        # Threads: client <-> backend server
        client_to_be = threading.Thread(target=forward_request, args=(client_conn, self.be_conn))
        be_to_client = threading.Thread(target=forward_request, args=(self.be_conn, client_conn))
        
        # Start thread execution
        client_to_be.start()
        be_to_client.start()
        
        # Wait for the thread to end
        client_to_be.join()
        be_to_client.join()
        
        # Close the connection
        client_conn.close()
        self.be_conn.close()

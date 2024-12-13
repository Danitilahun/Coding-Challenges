class RoundRobin:
    def __init__(self, servers):
        self.servers = servers
        self.current_index = 0

    def get_next_server(self):
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

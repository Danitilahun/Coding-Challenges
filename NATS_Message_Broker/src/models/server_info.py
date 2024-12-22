from dataclasses import dataclass

@dataclass
class ServerInfo:
    server_id: str

    server_name: str

    version: str

    go: str

    host: str

    port: int

    headers: bool

    max_payload: int

    proto: int

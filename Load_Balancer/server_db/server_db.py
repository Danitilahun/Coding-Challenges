import json

SERVER_DB = "./server_db/server_db.json"

def load_serverdb(server_db):
    server_info = {}
    with open(server_db, encoding="utf-8") as f:
        server_info = json.load(f)
    return server_info

server_info = load_serverdb(SERVER_DB)
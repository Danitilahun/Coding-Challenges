import json

SERVER_DB = "./src/server_db/server_db.json"

def load_serverdb(server_db: str) -> dict:
    """
    Load the server database from a JSON file.

    Args:
        server_db (str): The file path to the server database JSON file.

    Returns:
        dict: A dictionary containing the server information.

    Raises:
        FileNotFoundError: If the specified JSON file does not exist.
        json.JSONDecodeError: If the JSON file cannot be decoded.
    """
    with open(server_db, encoding="utf-8") as f:
        server_info = json.load(f)
    return server_info


server_info = load_serverdb(SERVER_DB)

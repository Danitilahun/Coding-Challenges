import json
import socket
import uuid
from typing import Dict

from src.client.client import Client
from src.constants.kind import Kind
from src.models.subscription import Subscription
from src.models.topic import Topic
from src.protocols.parser import Parser
from src.messages.message import Message
from utils.arg_parsers import parse_sub, parse_unsub_arg

class NATSServer:
    """
    Represents the NATS server for managing client connections and messaging.

    Attributes:
        server (socket.socket): The server socket instance.
        clients (Dict[str, Client]): A map of connected clients.
        topics (Dict[str, Topic]): A map of topics.
        subscriptions (Dict[int, Subscription]): A map of subscriptions by ID.
        debug (bool): Flag for enabling debug mode.
        server_info (dict): Information about the server.
    """

    def __init__(self, port: int, host: str = "0.0.0.0", debug: bool = False):
        """
        Initializes the NATS server.

        Args:
            port (int): The port to listen on.
            host (str): The host to bind to (default: "0.0.0.0").
            debug (bool): Enable debug mode (default: False).
        """
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients: Dict[str, Client] = {}
        self.topics: Dict[str, Topic] = {}
        self.subscriptions: Dict[int, Subscription] = {}
        self.debug = debug
        self.server_info = {
            "server_id": uuid.uuid4().hex,
            "server_name": host,
            "version": "2.6.1",
            "go": "go1.21.1",
            "host": host,
            "port": port,
            "headers": False,
            "max_payload": 1024 * 30,
            "proto": 1,
        }

    def start_server(self):
        """
        Starts the server and begins listening for client connections.
        """
        self.server.bind((self.server_info["host"], self.server_info["port"]))
        self.server.listen(5)
        print(f"Server started at {self.server_info['host']}:{self.server_info['port']}")

        while True:
            conn, addr = self.server.accept()
            
                
            client_key = f"{addr[0]}:{addr[1]}"
            
            if self.debug:
                print(f"Client connected: {client_key}")
                
            client = Client(client_key, conn)
            
            self.clients[client_key] = client


            parser = Parser(lambda msg: self.handle_message(msg, client))

            self.handle_client(client, parser)

    def handle_client(self, client: Client, parser: Parser):
        """
        Handles incoming client data and manages the connection.

        Args:
            client (Client): The connected client.
            parser (Parser): The parser instance for this client.
        """
        try:
            while True:
                data = client.connection.recv(1024)
                if not data:
                    break

                if self.debug:
                    print(f"Received from {client.key}: {data.decode()}")

                parser.parse(data)

        except Exception as e:
            if self.debug:
                print(f"Error with client {client.key}: {e}")
        finally:
            client.connection.close()
            del self.clients[client.key]
            if self.debug:
                print(f"Client disconnected: {client.key}")

    async def handle_message(self, msg: Message, client: Client):
        """
        Processes a message received from a client.

        Args:
            msg (Message): The message object.
            client (Client): The client who sent the message.
        """
        if msg.kind == Kind.PING:
            client.send_pong()
        elif msg.kind == Kind.CONNECT:
            self.handle_connect(msg,client)
        elif msg.kind == Kind.SUB:
            self.handle_sub(msg,client)
        elif msg.kind == Kind.PUB:
            await self.handle_pub(msg,client)
        elif msg.kind == Kind.UNSUB:
            self.handle_unsub(msg,client)
    
    def handle_connect(self, msg: Message, client: Client):
        """
        Handles the CONNECT command.

        Args:
            msg (Message): The CONNECT message.
            client (Client): The client sending the command.
        """
        new_options = json.loads(msg.data.decode())
        client.update_options(new_options)
        self.clients[client.key] = client
        client.send_ok()

    def handle_sub(self, msg: Message, client: Client):
        """
        Handles the SUB command.

        Args:
            msg (Message): The SUB message.
            client (Client): The client sending the command.
        """
        sub_arg = parse_sub(msg.data)
        subject = sub_arg.subject.decode()
        topic_key = subject

        topic = self.topics.get(topic_key)
        subscription = Subscription(client, sub_arg.sid, subject)

        if topic:
            topic.sub(subscription)
        else:
            topic = Topic(subject)
            topic.sub(subscription)
            self.topics[topic_key] = topic

        self.subscriptions[sub_arg.sid] = subscription
        client.send_ok()

    def handle_unsub(self, msg: Message, client: Client):
        """
        Handles the UNSUB command.

        Args:
            msg (Message): The UNSUB message.
            client (Client): The client sending the command.
        """
        unsub_arg = parse_unsub_arg(msg.data)
        subscription = self.subscriptions.get(unsub_arg.sid)

        if subscription is None:
            return

        topic = self.topics.get(subscription.subject)
        if topic is None:
            return

        topic.unsub(subscription)
        client.send_ok()

    async def handle_pub(self, msg: Message, client: Client):
        """
        Handles the PUB command.

        Args:
            msg (Message): The PUB message.
            client (Client): The client sending the command.
        """
        pub_arg = msg.pub_arg
        subject = pub_arg.subject.decode()
        topic = self.topics.get(subject)

        if topic is None:
            return

        client.send_ok()
        await topic.publish(pub_arg)

    def send_info(self, client: Client):
        """
        Sends the INFO message to the client.

        Args:
            client (Client): The client to send the INFO message to.
        """
        client.connection.sendall(f"INFO {json.dumps(self.server_info)}\r\n".encode())

    async def stop_server(self):
        """
        Stops the server gracefully.
        """
        self.server.close()
        print("Server stopped.")
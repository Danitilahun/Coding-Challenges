"""
This module defines the State enum, which represents the states of the
NATS message parser.

Example:
    - State.OP_START: The parser is waiting for the start of a command.
    - State.MSG_PAYLOAD: The parser is processing the payload of a message.
"""

from enum import Enum

class State(Enum):
    """
    Represents the states of the message parser while processing commands.

    Usage:
        The parser transitions between these states based on the incoming
        stream of bytes to interpret and execute commands.
    """
    OP_START = 0      # Initial state
    OP_C = 1          # Parsing "C"
    OP_CO = 2         # Parsing "CO"
    OP_CON = 3        # Parsing "CON"
    OP_CONN = 4       # Parsing "CONN"
    OP_CONNE = 5      # Parsing "CONNE"
    OP_CONNEC = 6     # Parsing "CONNEC"
    OP_CONNECT = 7    # Parsing "CONNECT"
    CONNECT_ARG = 8   # Parsing CONNECT arguments
    OP_P = 9          # Parsing "P"
    OP_PI = 10        # Parsing "PI"
    OP_PIN = 11       # Parsing "PIN"
    OP_PING = 12      # Parsing "PING"
    OP_PO = 13        # Parsing "PO"
    OP_PON = 14       # Parsing "PON"
    OP_PONG = 15      # Parsing "PONG"
    OP_S = 16         # Parsing "S"
    OP_SU = 17        # Parsing "SU"
    OP_SUB = 18       # Parsing "SUB"
    SUB_ARG = 19      # Parsing SUB arguments
    OP_PU = 20        # Parsing "PU"
    OP_PUB = 21       # Parsing "PUB"
    PUB_ARG = 22      # Parsing PUB arguments
    MSG_PAYLOAD = 23  # Parsing message payload
    MSG_END_CR = 24   # Parsing message end with CR
    MSG_END_LF = 25   # Parsing message end with LF
    OP_U = 26         # Parsing "U"
    OP_UN = 27        # Parsing "UN"
    OP_UNS = 28       # Parsing "UNS"
    OP_UNSU = 29      # Parsing "UNSU"
    OP_UNSUB = 30     # Parsing "UNSUB"
    UNSUB_ARG = 31    # Parsing UNSUB arguments

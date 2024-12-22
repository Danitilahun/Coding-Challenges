from dataclasses import dataclass, field
from typing import Optional

@dataclass
class ClientOptions:
    """
    Represents the configuration options for a client.

    Attributes:
        verbose (bool): Indicates whether verbose mode is enabled.
        pedantic (bool): Enables pedantic mode for strict protocol adherence.
        tls_required (bool): Specifies if TLS is required for the connection.
        auth_token (Optional[str]): Authentication token for client connection (if any).
        user (Optional[str]): Username for authentication.
        password (Optional[str]): Password for authentication.
        name (Optional[str]): Name of the client instance.
        lang (str): Language of the client implementation (e.g., Python).
        version (str): Version of the client implementation.
        protocol (Optional[int]): Protocol version supported by the client.
        echo (Optional[bool]): Determines if the client echoes its own messages.
        sig (Optional[str]): Digital signature for client verification.
        jwt (Optional[str]): JSON Web Token for authentication.
        no_responders (Optional[bool]): Indicates if responders are disabled.
        headers (Optional[bool]): Specifies if headers are supported in the protocol.
        nkey (Optional[str]): Public key for client identification.
    """
    verbose: bool
    pedantic: bool
    tls_required: bool
    auth_token: Optional[str] = None
    user: Optional[str] = None
    password: Optional[str] = None
    name: Optional[str] = None
    lang: str = ""
    version: str = ""
    protocol: Optional[int] = None
    echo: Optional[bool] = None
    sig: Optional[str] = None
    jwt: Optional[str] = None
    no_responders: Optional[bool] = None
    headers: Optional[bool] = None
    nkey: Optional[str] = None

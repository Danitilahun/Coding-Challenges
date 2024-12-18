import hashlib
import base64
import random


def generate_short_url_key(long_url: str) -> str:
    """
    Generates a shortened URL key from a given long URL.
    Steps:
        1. Hash the URL using SHA-256.
        2. Encode the hash using Base64.
        3. Shuffle the characters for randomness.
        4. Remove non-URL-safe characters like '/' and '='.
        5. Trim the result to 7 characters.

    Args:
        long_url (str): The original long URL.

    Returns:
        str: A 7-character short key for the URL.
    """
    hashed_string = hashlib.sha256(long_url.encode('utf-8')).digest()

    b64 = base64.b64encode(hashed_string).decode('utf-8')

    shuffle = ''.join(random.sample(b64, len(b64)))

    final_url = shuffle.replace("/", "").replace("=", "")

    return final_url[:7]

from typing import Dict

from src.huffman.huffman_trees import HuffmanTree


class CompressionUtils:
    """
    Utility class containing methods related to the compression process in Huffman Coding.
    """

    @staticmethod
    def create_frequency_dict(text: str) -> Dict[str, int]:
        """
        Creates a frequency dictionary mapping each character in the text to its frequency.

        Args:
            text (str): The input text for which the frequency map is to be created.

        Returns:
            Dict[str, int]: A dictionary with characters as keys and their frequencies as values.
        """
        frequency: Dict[str, int] = {}
        for character in text:
            if character not in frequency:
                frequency[character] = 0
            frequency[character] += 1
        return frequency

    @staticmethod
    def encode_text(text: str, code_table: Dict[str, str]) -> str:
        """
        Encodes the input text using the provided Huffman codes.

        Args:
            text (str): The input text to encode.
            code_table (Dict[str, str]): The Huffman codes for each character.

        Returns:
            str: The encoded text as a binary string.
        """
        return ''.join(code_table[char] for char in text)

    @staticmethod
    def pad_encoded_text(encoded_text: str) -> str:
        """
        Pads the encoded text to make its length a multiple of 8 bits.

        The first 8 bits store the number of padding bits added.

        Args:
            encoded_text (str): The binary string to pad.

        Returns:
            str: The padded binary string with padding information.
        """
        extra_padding = 8 - len(encoded_text) % 8
        if extra_padding == 8:
            extra_padding = 0  # No padding needed

        padded_encoded_text = encoded_text + "0" * extra_padding
        padded_info = f"{extra_padding:08b}"
        padded_encoded_text = padded_info + padded_encoded_text
        return padded_encoded_text

    @staticmethod
    def get_byte_array(padded_encoded_text: str) -> bytearray:
        """
        Converts the padded encoded text into a byte array.

        Args:
            padded_encoded_text (str): The padded binary string.

        Returns:
            bytearray: The byte array representation of the padded encoded text.
        """
        if len(padded_encoded_text) % 8 != 0:
            raise ValueError("Encoded text not padded properly")

        byte_array = bytearray()
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i+8]
            byte_array.append(int(byte, 2))
        return byte_array

    @staticmethod
    def serialize_frequency_map(frequency_map: Dict[str, int]) -> bytes:
        """
        Serializes the frequency map to bytes for storage in the compressed file.

        Args:
            frequency_map (Dict[str, int]): The frequency map to serialize.

        Returns:
            bytes: The serialized frequency map.
        """
        tree = HuffmanTree(frequencies=frequency_map)
        return tree.serialize_frequency_map()

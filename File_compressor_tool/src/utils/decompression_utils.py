from typing import Dict

from src.huffman.huffman_trees import HuffmanTree


class DecompressionUtils:
    """
    Utility class containing methods related to the decompression process in Huffman Coding.
    """

    @staticmethod
    def remove_padding(padded_encoded_text: str) -> str:
        """
        Removes the padding from the encoded text.

        Args:
            padded_encoded_text (str): The padded binary string.

        Returns:
            str: The binary string without padding.
        """
        padded_info = padded_encoded_text[:8]
        extra_padding = int(padded_info, 2)

        encoded_text = padded_encoded_text[8:]
        if extra_padding > 0:
            encoded_text = encoded_text[:-extra_padding]
        return encoded_text

    @staticmethod
    def decode_text(encoded_text: str, reverse_code_table: Dict[str, str]) -> str:
        """
        Decodes the binary string back to the original text using the reverse mapping.

        Args:
            encoded_text (str): The binary string to decode.
            reverse_code_table (Dict[str, str]): Mapping from Huffman codes to characters.

        Returns:
            str: The decoded original text.
        """
        current_code = ""
        decoded_text = ""

        for bit in encoded_text:
            current_code += bit
            if current_code in reverse_code_table:
                character = reverse_code_table[current_code]
                decoded_text += character
                current_code = ""

        return decoded_text

    @staticmethod
    def deserialize_frequency_map(data: bytes) -> Dict[str, int]:
        """
        Deserializes the frequency map from bytes.

        Args:
            data (bytes): The bytes containing the serialized frequency map.

        Returns:
            Dict[str, int]: The deserialized frequency map.
        """
        return HuffmanTree.deserialize_frequency_map(data)

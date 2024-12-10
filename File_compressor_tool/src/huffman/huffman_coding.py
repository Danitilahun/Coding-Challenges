import os
import struct
from typing import Optional

from src.huffman.huffman_trees import HuffmanTree
from src.utils.compression_utils import CompressionUtils
from src.utils.decompression_utils import DecompressionUtils


class HuffmanCoding:
    """
    Handles the compression and decompression processes using Huffman Coding.

    Attributes:
        file_path (str): The path to the file to compress or decompress.
        tree (Optional[HuffmanTree]): The HuffmanTree instance used for encoding/decoding.
    """

    def __init__(self, file_path: str):
        """
        Initializes the HuffmanCoding instance with the specified file path.

        Args:
            file_path (str): The path to the file to compress or decompress.
        """
        self.file_path: str = file_path
        self.tree: Optional[HuffmanTree] = None

    def compress(self, output_path: str) -> str:
        """
        Compresses the file at the given path using Huffman Coding.

        The compressed file format:
            [frequency_map_size][frequency_map][padded_encoded_text]

        Args:
            output_path (str): The path where the compressed binary file will be saved.

        Returns:
            str: The path to the compressed binary file.
        """
        with open(self.file_path, 'r', encoding='utf-8') as file:
            text = file.read().rstrip()

        frequency = CompressionUtils.create_frequency_dict(text)

        self.tree = HuffmanTree(frequencies=frequency)
        self.tree.build_tree()
        self.tree.generate_code_tables()

        encoded_text = CompressionUtils.encode_text(text, self.tree.get_code_table())

        padded_encoded_text = CompressionUtils.pad_encoded_text(encoded_text)

        byte_array = CompressionUtils.get_byte_array(padded_encoded_text)

        serialized_frequency = CompressionUtils.serialize_frequency_map(frequency)

        with open(output_path, 'wb') as output:
            
            output.write(struct.pack('>I', len(serialized_frequency)))
            
            output.write(serialized_frequency)
            
            output.write(bytes(byte_array))
            
        print(f"Compressed '{self.file_path}' to '{output_path}'")
        
        return output_path

    def decompress(self, input_path: str, output_path: str) -> str:
        """
        Decompresses the binary file at the given path back to the original text.

        The compressed file format should be:
            [frequency_map_size][frequency_map][padded_encoded_text]

        Args:
            input_path (str): The path to the compressed binary file.
            output_path (str): The path where the decompressed text file will be saved.

        Returns:
            str: The path to the decompressed text file.
        """
        with open(input_path, 'rb') as file:
            
            frequency_map_size_bytes = file.read(4)
            if len(frequency_map_size_bytes) < 4:
                raise ValueError("Invalid compressed file format.")

            frequency_map_size = struct.unpack('>I', frequency_map_size_bytes)[0]

            serialized_frequency = file.read(frequency_map_size)
            frequency_map = DecompressionUtils.deserialize_frequency_map(serialized_frequency)

            self.tree = HuffmanTree(frequencies=frequency_map)
            self.tree.build_tree()
            self.tree.generate_code_tables()

            byte_array = file.read()
            padded_encoded_text = ''.join(f"{byte:08b}" for byte in byte_array)

            encoded_text = DecompressionUtils.remove_padding(padded_encoded_text)

            decoded_text = DecompressionUtils.decode_text(encoded_text, self.tree.get_reverse_code_table())

        with open(output_path, 'w', encoding='utf-8') as output:
            output.write(decoded_text)

        print(f"Decompressed '{input_path}' to '{output_path}'")
        
        return output_path

import heapq
import struct
from typing import Dict, Optional
from src.huffman.huffman_node import HuffmanNode


class HuffmanTree:
    """
    Represents the Huffman Tree used for encoding and decoding.

    Attributes:
        frequencies (Dict[str, int]): Mapping of characters to their frequencies.
        root (Optional[HuffmanNode]): The root node of the Huffman Tree.
        code_table (Dict[str, str]): Mapping of characters to their Huffman codes.
        reverse_code_table (Dict[str, str]): Mapping of Huffman codes to their characters.
    """

    def __init__(self, frequencies: Dict[str, int]):
        """
        Initializes the HuffmanTree with a frequency dictionary.

        Args:
            frequencies (Dict[str, int]): A dictionary with characters as keys and their frequencies as values.
        """
        self.frequencies: Dict[str, int] = frequencies
        self.root: Optional[HuffmanNode] = None
        self.code_table: Dict[str, str] = {}
        self.reverse_code_table: Dict[str, str] = {}

    def build_tree(self) -> None:
        """
        Builds the Huffman Tree using the provided frequencies.
        
        Raises:
            ValueError: If any frequency is non-positive.
        """
        priority_queue: list[HuffmanNode] = []

        for char, freq in self.frequencies.items():
            if freq <= 0:
                raise ValueError(f"Invalid frequency for character '{char}': {freq}. Must be positive.")
            heapq.heappush(priority_queue, HuffmanNode(weight=freq, element=char))

        if not priority_queue:
            self.root = None
            return

        while len(priority_queue) > 1:
            left: HuffmanNode = heapq.heappop(priority_queue)
            right: HuffmanNode = heapq.heappop(priority_queue)
            merged_weight = left.weight + right.weight
            merged_node = HuffmanNode(weight=merged_weight, left=left, right=right)
            heapq.heappush(priority_queue, merged_node)

        self.root = heapq.heappop(priority_queue)

    def generate_code_tables(self) -> None:
        """
        Generates the prefix and reverse code tables by traversing the Huffman Tree.
        """
        if self.root is not None:
            self._generate_codes_helper(node=self.root, current_code="")

    def _generate_codes_helper(self, node: Optional[HuffmanNode], current_code: str) -> None:
        """
        Recursively traverses the Huffman Tree to generate Huffman codes.

        Args:
            node (Optional[HuffmanNode]): The current node in the Huffman Tree.
            current_code (str): The current Huffman code string being built.
        """
        if node is None:
            return

        if node.is_leaf():
            self.code_table[node.element] = current_code or "0"
            self.reverse_code_table[current_code or "0"] = node.element
            return

        if node.left:
            self._generate_codes_helper(node.left, current_code + "0")
        if node.right:
            self._generate_codes_helper(node.right, current_code + "1")

    def get_code_table(self) -> Dict[str, str]:
        """
        Retrieves the generated Huffman codes for each character.

        Returns:
            Dict[str, str]: A dictionary mapping characters to their Huffman codes.
        """
        return self.code_table

    def get_reverse_code_table(self) -> Dict[str, str]:
        """
        Retrieves the reverse mapping from Huffman codes to characters.

        Returns:
            Dict[str, str]: A dictionary mapping Huffman codes to their corresponding characters.
        """
        return self.reverse_code_table

    def serialize_frequency_map(self) -> bytes:
        """
        Serializes the frequency map to bytes for storage in the compressed file.

        Format:
            [number_of_unique_chars][char1][freq1][char2][freq2]...

        Returns:
            bytes: The serialized frequency map.
        """

        serialized_data = bytearray()
        num_chars = len(self.frequencies)
        serialized_data.extend(struct.pack('>I', num_chars))

        for char, freq in self.frequencies.items():
            char_bytes = char.encode('utf-8')
            char_length = len(char_bytes)
            serialized_data.extend(struct.pack('>H', char_length))  # 2 bytes for the length of the character
            serialized_data.extend(char_bytes)                      # character bytes
            serialized_data.extend(struct.pack('>I', freq))        # 4 bytes for frequency

        return bytes(serialized_data)

    @staticmethod
    def deserialize_frequency_map(data: bytes) -> Dict[str, int]:
        """
        Deserializes the frequency map from bytes.

        Args:
            data (bytes): The bytes containing the serialized frequency map.

        Returns:
            Dict[str, int]: The deserialized frequency map.
        """
        import struct

        frequency_map: Dict[str, int] = {}
        offset = 0
        num_chars = struct.unpack('>I', data[offset:offset+4])[0]
        offset += 4

        for _ in range(num_chars):
            char_length = struct.unpack('>H', data[offset:offset+2])[0]
            offset += 2
            char = data[offset:offset+char_length].decode('utf-8')
            offset += char_length
            freq = struct.unpack('>I', data[offset:offset+4])[0]
            offset += 4
            frequency_map[char] = freq

        return frequency_map

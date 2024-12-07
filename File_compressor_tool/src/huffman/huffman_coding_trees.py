import heapq
from typing import Dict, Optional
from src.huffman.huffman_node import HuffmanNode


class HuffmanTree:
    def __init__(self, frequencies: Dict[str, int]):
        """
        Initialize the Huffman tree with a frequency dictionary.
        :param frequencies: A dictionary with characters as keys and their frequencies as values.
        """
        self.frequencies: Dict[str, int] = frequencies
        self.root: Optional[HuffmanNode] = None

    def build_tree(self) -> None:
        """
        Build the Huffman tree using the provided frequencies.
        :return: None
        """
        # Priority queue (min-heap) to store Huffman nodes
        priority_queue: list[HuffmanNode] = []

        for char, freq in self.frequencies.items():
            heapq.heappush(priority_queue, HuffmanNode(freq, char))

        while len(priority_queue) > 1:
            left: HuffmanNode = heapq.heappop(priority_queue)
            right: HuffmanNode = heapq.heappop(priority_queue)

            merged = HuffmanNode(left.weight + right.weight,
                                 left=left, right=right)

            heapq.heappush(priority_queue, merged)

        self.root = heapq.heappop(priority_queue)

    def generate_prefix_code_table(self, node=None, prefix="") -> Dict[str, str]:
        """
        Generate a prefix-code table by traversing the Huffman tree.

        Args:
            node (Optional[HuffmanNode]): The current node in the tree. Defaults to root.
            prefix (str): The binary code prefix for the current node.

        Returns:
            dict: A dictionary mapping characters to their binary codes.
        """
        if node is None:
            node = self.root

        code_table = {}

        if node.is_leaf():
            code_table[node.element] = prefix
        else:

            code_table.update(self.generate_prefix_code_table(
                node.left, prefix + "0"))
            code_table.update(self.generate_prefix_code_table(
                node.right, prefix + "1"))

        return code_table

    def serialize_tree(self, node=None) -> str:
        """
        Serialize the Huffman tree using pre-order traversal.

        Args:
            node (Optional[HuffmanNode]): The root node to start serialization (default is the tree's root).

        Returns:
            str: A serialized string representation of the Huffman tree.
        """
        if node is None:
            node = self.root

        if node.is_leaf():
            return f"L{repr(node.element)}"
        else:
            return f"I{self.serialize_tree(node.left)}{self.serialize_tree(node.right)}"
        
    

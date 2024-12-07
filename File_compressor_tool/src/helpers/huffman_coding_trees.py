import heapq
from typing import Dict, Optional


class HuffmanNode:
    def __init__(self, weight: int, element: Optional[str] = None, 
                 left: Optional['HuffmanNode'] = None, 
                 right: Optional['HuffmanNode'] = None):
        """
        Constructor for a Huffman node.
        :param weight: The weight (frequency) of the node.
        :param element: The character element for this node (None for internal nodes).
        :param left: Left child node (None for leaf nodes).
        :param right: Right child node (None for leaf nodes).
        """
        self.weight: int = weight
        self.element: Optional[str] = element
        self.left: Optional[HuffmanNode] = left
        self.right: Optional[HuffmanNode] = right

    def is_leaf(self) -> bool:
        """
        Check if this node is a leaf.
        :return: True if this is a leaf node (no children), otherwise False.
        """
        return self.left is None and self.right is None

    def __lt__(self, other: 'HuffmanNode') -> bool:
        """
        Comparator for priority queue (heapq).
        :param other: Another HuffmanNode to compare against.
        :return: True if this node's weight is less than the other node's weight.
        """
        return self.weight < other.weight


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

            merged = HuffmanNode(left.weight + right.weight, left=left, right=right)

            heapq.heappush(priority_queue, merged)

        self.root = heapq.heappop(priority_queue)

    def print_codes(self, node: Optional[HuffmanNode] = None, prefix: str = "") -> None:
        """
        Recursively print the Huffman codes.
        :param node: The current Huffman node. Defaults to the root node.
        :param prefix: The binary code prefix for the current node.
        :return: None
        """
        if node is None:
            node = self.root

        if node.is_leaf():
            print(f"Character: {node.element}, Code: {prefix}")
        else:
            self.print_codes(node.left, prefix + "0")
            self.print_codes(node.right, prefix + "1")

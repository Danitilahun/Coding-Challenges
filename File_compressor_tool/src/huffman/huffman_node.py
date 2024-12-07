# src/huffman/huffman_node.py
import itertools
from typing import Optional

class HuffmanNode:
    _counter = itertools.count()  # Unique sequence count

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
        self.left: Optional['HuffmanNode'] = left
        self.right: Optional['HuffmanNode'] = right
        self.order = next(HuffmanNode._counter) 

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
        if self.weight != other.weight:
            return self.weight < other.weight
        return self.order < other.order

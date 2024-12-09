from typing import Optional


class HuffmanNode:
    """
    Represents a node in the Huffman Tree.

    Attributes:
        weight (int): The frequency of the character or the sum of frequencies for internal nodes.
        element (Optional[str]): The character this node represents (None for internal nodes).
        left (Optional[HuffmanNode]): The left child node.
        right (Optional[HuffmanNode]): The right child node.
    """

    def __init__(
        self,
        weight: int,
        element: Optional[str] = None,
        left: Optional['HuffmanNode'] = None,
        right: Optional['HuffmanNode'] = None
    ):
        """
        Initializes a HuffmanNode instance.

        Args:
            weight (int): The frequency of the character or the combined frequency for internal nodes.
            element (Optional[str], optional): The character. Defaults to None for internal nodes.
            left (Optional[HuffmanNode], optional): Left child node. Defaults to None.
            right (Optional[HuffmanNode], optional): Right child node. Defaults to None.
            
        Raises:
            ValueError: If weight is not a positive integer.
        """
        
        if weight < 0:
            raise ValueError("Weight must be a non-negative integer.")
        self.weight: int = weight
        self.element: Optional[str] = element
        self.left: Optional['HuffmanNode'] = left
        self.right: Optional['HuffmanNode'] = right

    def is_leaf(self) -> bool:
        """
        Determines if the node is a leaf node.

        Returns:
            bool: True if the node is a leaf (has no children), False otherwise.
        """
        return self.left is None and self.right is None

    def __lt__(self, other: object) -> bool:
        """
        Less-than comparison based on node weight for priority queue ordering.

        Args:
            other (object): Another HuffmanNode to compare with.

        Returns:
            bool: True if this node's weight is less than the other's weight, False otherwise.

        Raises:
            TypeError: If 'other' is not a HuffmanNode instance.
        """
        if not isinstance(other, HuffmanNode):
            return NotImplemented
        if self.weight != other.weight:
            return self.weight < other.weight
        return False


    def __eq__(self, other: object) -> bool:
        """
        Equality comparison based on node weight.

        Args:
            other (object): Another object to compare with.

        Returns:
            bool: True if both nodes have the same weight, False otherwise.
        """
        if not isinstance(other, HuffmanNode):
            return False
        return self.weight == other.weight

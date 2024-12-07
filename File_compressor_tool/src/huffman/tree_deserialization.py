import ast
from typing import Tuple
from src.huffman.huffman_node import HuffmanNode

def deserialize_tree(serialized_str: str) -> HuffmanNode:
    """
    Deserialize a Huffman tree from the given serialized string.

    The format is:
    - 'I' for internal nodes followed by the serialization of left and right subtrees.
    - 'L' for leaf nodes followed by repr(node.element).

    Args:
        serialized_str (str): The serialized string of the Huffman tree.

    Returns:
        HuffmanNode: The root of the deserialized Huffman tree.
    """
   
    def _deserialize(index: int) -> Tuple[HuffmanNode, int]:
        if index >= len(serialized_str):
            raise ValueError("Invalid serialized string: ran out of data prematurely.")
        
        node_type = serialized_str[index]
        index += 1

        if node_type == 'L':
            # Leaf node: the next part is the repr of the element.
            # We need to parse until we get a valid repr. The safest way is:
            # 1. Extract the remainder of the string.
            # 2. Use a balanced approach to find the closing quote.
            
            # The next characters should represent the node's element in repr form.
            # Example: L'a' or L"abc"
            # We'll assume that the element is always a single character or string in quotes.
            # We can try to parse from the current index until we successfully evaluate it.

            # Extract the substring for the element:
            # Since we used repr, it starts with a quote (' or ") and ends with a matching one.
            # Let's find the end of this repr segment. The first character should be a quote.
            if index >= len(serialized_str):
                raise ValueError("Invalid leaf node: no element data found.")

            # Identify the starting quote
            start_quote = serialized_str[index]
            if start_quote not in ["'", '"']:
                raise ValueError(f"Invalid leaf node: expected quote, got {start_quote}")

            # Find the matching end quote
            end_pos = index + 1
            while end_pos < len(serialized_str):
                if serialized_str[end_pos] == start_quote and serialized_str[end_pos - 1] != '\\':
                    break
                end_pos += 1

            if end_pos >= len(serialized_str):
                raise ValueError("Invalid leaf node: could not find closing quote for element.")

            element_str = serialized_str[index:end_pos+1]
            index = end_pos + 1

            element = ast.literal_eval(element_str)

            return HuffmanNode(weight=0, element=element), index

        elif node_type == 'I':
            left_node, index = _deserialize(index)
            right_node, index = _deserialize(index)
          
            node = HuffmanNode(left_node.weight + right_node.weight, left=left_node, right=right_node)
            return node, index
        else:
            raise ValueError(f"Invalid node type '{node_type}' encountered during deserialization.")


    root, final_index = _deserialize(0)
    if final_index != len(serialized_str):
        raise ValueError("Extra data found after deserializing the Huffman tree.")

    return root

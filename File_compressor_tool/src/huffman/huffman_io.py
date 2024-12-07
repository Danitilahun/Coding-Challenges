from src.huffman.huffman_coding_trees import HuffmanTree
from src.huffman.tree_deserialization import deserialize_tree
from src.huffman.huffman_node import HuffmanNode

def write_compressed_file(output_filename: str, huffman_tree: HuffmanTree, compressed_data: str) -> None:
    """
    Writes the compressed file with a header containing the serialized Huffman tree.

    Args:
        output_filename (str): The output file name.
        huffman_tree (HuffmanTree): The Huffman tree used for compression.
        compressed_data (str): The compressed binary string.
    """
    serialized_tree = huffman_tree.serialize_tree()

    with open(output_filename, "wb") as file:
        file.write(f"{serialized_tree}\n".encode())
        file.write(b"---END_HEADER---\n")
        file.write(compressed_data.encode())

def read_compressed_file(input_filename: str) -> tuple[HuffmanNode, str]:
    """
    Reads the compressed file and extracts the Huffman tree and compressed data.

    Args:
        input_filename (str): The input file name.

    Returns:
        tuple[HuffmanNode, str]: A tuple containing the Huffman tree and the compressed binary string.
    """
    with open(input_filename, "rb") as file:
        serialized_tree = ""
        for line in file:
            if line.strip() == b"---END_HEADER---":
                break
            serialized_tree += line.decode().strip()

        huffman_tree_root = deserialize_tree(serialized_tree)
        compressed_data = file.read().decode()

    return huffman_tree_root, compressed_data

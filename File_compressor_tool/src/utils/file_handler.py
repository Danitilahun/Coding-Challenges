import os
from src.huffman.huffman_coding_trees import HuffmanTree
from src.huffman.tree_deserialization import deserialize_tree
from src.huffman.huffman_node import HuffmanNode

def process_file(filename: str) -> str:
    """
    Processes the input file. If invalid, raises appropriate exceptions.

    Args:
        filename (str): The name of the file to be processed.

    Returns:
        str: The content of the file.

    Raises:
        FileNotFoundError: If the file does not exist.
        IsADirectoryError: If the filename points to a directory instead of a file.
        UnicodeDecodeError: If the file contains undecodable characters.
        IOError: If the file cannot be opened.
    """
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Error: File '{filename}' does not exist.")
    
    if not os.path.isfile(filename):
        raise IsADirectoryError(f"Error: '{filename}' is not a valid file.")
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
            return content
    except UnicodeDecodeError as e:
        raise UnicodeDecodeError(
            e.encoding,
            e.object,
            e.start,
            e.end,
            f"Error: Unable to decode the file '{filename}'. "
            f"Character at position {e.start}-{e.end} could not be decoded. "
            f"Details: {str(e)}"
        )
    except IOError as e:
        raise IOError(f"Error: Unable to open the file '{filename}'. Details: {str(e)}")

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

from src.huffman.huffman_coding_trees import HuffmanTree
from src.utils.file_handler import process_file, read_compressed_file, write_compressed_file


def process_and_compress(input_filename: str, output_filename: str) -> None:
    """
    Compresses the input file using Huffman coding and writes the compressed file.

    Args:
        input_filename (str): Path to the input file.
        output_filename (str): Path to the compressed output file.
    """
    content = process_file(input_filename)

    frequency_table = {}
    for char in content:
        frequency_table[char] = frequency_table.get(char, 0) + 1

    huffman_tree = HuffmanTree(frequency_table)
    huffman_tree.build_tree()

    prefix_code_table = huffman_tree.generate_prefix_code_table()

    compressed_data = ''.join(prefix_code_table[char] for char in content)

    write_compressed_file(output_filename, huffman_tree, compressed_data)


def process_and_decompress(input_filename: str, output_filename: str) -> None:
    """
    Decompresses a compressed file using Huffman coding and writes the decompressed content.

    Args:
        input_filename (str): Path to the compressed input file.
        output_filename (str): Path to the decompressed output file.
    """
    huffman_tree_root, compressed_data = read_compressed_file(input_filename)

    decompressed_content = []
    node = huffman_tree_root
    for bit in compressed_data:
        node = node.left if bit == '0' else node.right
        if node.is_leaf():
            decompressed_content.append(node.element)
            node = huffman_tree_root

    with open(output_filename, "w", encoding="utf-8") as file:
        file.write(''.join(decompressed_content))

# main.py
import sys
import os
import argparse
from src.huffman.huffman_coding import HuffmanCoding


def main():
    """
    The main function that parses command-line arguments and performs compression or decompression.
    """
    parser = argparse.ArgumentParser(description="Huffman Coding Compression and Decompression Tool")
    subparsers = parser.add_subparsers(dest='action', help='Action to perform')

    # Parser for compression
    compress_parser = subparsers.add_parser('compress', help='Compress a file')
    compress_parser.add_argument('input_filename', type=str, help='Path to the input file to compress')
    compress_parser.add_argument('output_filename', type=str, help='Path to save the compressed file')

    # Parser for decompression
    decompress_parser = subparsers.add_parser('decompress', help='Decompress a file')
    decompress_parser.add_argument('input_filename', type=str, help='Path to the compressed file to decompress')
    decompress_parser.add_argument('output_filename', type=str, help='Path to save the decompressed file')

    args = parser.parse_args()

    if not args.action:
        parser.print_help()
        sys.exit(1)

    action = args.action
    input_filename = args.input_filename
    output_filename = args.output_filename

    if not os.path.isfile(input_filename):
        print(f"Error: The file '{input_filename}' does not exist.")
        sys.exit(1)

    try:
        if action == 'compress':
            huffman_coding = HuffmanCoding(file_path=input_filename)
            compressed_file = huffman_coding.compress(output_path=output_filename)
            print(f"Compression successful. Compressed file saved as '{compressed_file}'.")
        elif action == 'decompress':
            huffman_coding = HuffmanCoding(file_path=input_filename)
            decompressed_file = huffman_coding.decompress(input_path=input_filename, output_path=output_filename)
            print(f"Decompression successful. Decompressed file saved as '{decompressed_file}'.")
    except Exception as e:
        print(f"An error occurred during {action}: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

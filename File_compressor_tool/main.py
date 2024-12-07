import sys
import os
from src.main_solution import process_and_compress, process_and_decompress


def main():
    if len(sys.argv) < 4:
        print("Usage: python main.py <compress|decompress> <input_filename> <output_filename>")
        sys.exit(1)

    action = sys.argv[1]
    input_filename = sys.argv[2]
    output_filename = sys.argv[3]

    if not os.path.isfile(input_filename):
        print(f"Error: The file '{input_filename}' does not exist.")
        sys.exit(1)

    try:
        if action == "compress":
            print(f"Compressing '{input_filename}' into '{output_filename}'...")
            process_and_compress(input_filename, output_filename)
            print("Compression successful!")

        elif action == "decompress":
            print(f"Decompressing '{input_filename}' into '{output_filename}'...")
            process_and_decompress(input_filename, output_filename)
            print("Decompression successful!")

        else:
            print("Error: Invalid action. Use 'compress' or 'decompress'.")
            sys.exit(1)

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

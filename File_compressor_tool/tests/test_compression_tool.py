import os
from src.main_solution import process_and_compress, process_and_decompress


def test_compression_tool():
    """
    Tests the compression tool by compressing and decompressing a file and verifying results.
    """
    # File paths
    input_filename = "data/input.txt"
    compressed_filename = "data/output.bin"
    decompressed_filename = "data/decompressed.txt"

    # Ensure input file exists
    if not os.path.isfile(input_filename):
        raise FileNotFoundError(f"Error: The file '{input_filename}' does not exist. Place an example input file in the 'data/' folder.")

    # Step 1: Compress the file
    print(f"Compressing '{input_filename}' into '{compressed_filename}'...")
    process_and_compress(input_filename, compressed_filename)
    print("Compression complete!")

    # Step 2: Decompress the file
    print(f"Decompressing '{compressed_filename}' into '{decompressed_filename}'...")
    process_and_decompress(compressed_filename, decompressed_filename)
    print("Decompression complete!")

    # Step 3: Compare file sizes
    original_size = os.path.getsize(input_filename)
    compressed_size = os.path.getsize(compressed_filename)
    decompressed_size = os.path.getsize(decompressed_filename)

    print("\nFile Size Comparison:")
    print(f"Original File Size: {original_size} bytes")
    print(f"Compressed File Size: {compressed_size} bytes")
    print(f"Decompressed File Size: {decompressed_size} bytes")

    # Step 4: Verify that the decompressed file matches the original
    with open(input_filename, "r", encoding="utf-8") as original_file, \
         open(decompressed_filename, "r", encoding="utf-8") as decompressed_file:
        original_content = original_file.read()
        decompressed_content = decompressed_file.read()

        assert original_content == decompressed_content, "Decompressed content does not match the original file."

    print("\nVerification: Success! The decompressed file matches the original file.")

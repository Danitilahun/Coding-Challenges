import argparse
import os
import sys
from ccwc_utils import count_bytes_from_stream, count_chars_from_stream, count_words_and_lines_from_stream


def create_parser():
    parser = argparse.ArgumentParser(
        description="Command-line Word Counter Tool")
    parser.add_argument("-c", "--bytes", action="store_true",
                        help="Outputs the number of bytes in the file or input")
    parser.add_argument("-m", "--chars", action="store_true",
                        help="Outputs the number of characters in the file or input")
    parser.add_argument("-w", "--words", action="store_true",
                        help="Outputs the number of words in the file or input")
    parser.add_argument("-l", "--lines", action="store_true",
                        help="Outputs the number of lines in the file or input")
    parser.add_argument("filename", nargs="?",
                        help="Name of the file to process (optional)")
    return parser


def process_input(input_stream, args):
    line_count = word_count = byte_count = char_count = 0

    if args.lines or args.words:
        line_count, word_count = count_words_and_lines_from_stream(input_stream)
        if line_count == -1 or word_count == -1:
            return

    input_stream.seek(0)

    if args.bytes:
        byte_count = count_bytes_from_stream(input_stream)
        if byte_count == -1:
            return

    input_stream.seek(0)

    if args.chars:
        char_count = count_chars_from_stream(input_stream)
        if char_count == -1:
            return

    output = []
    if args.lines:
        output.append(str(line_count))
    if args.words:
        output.append(str(word_count))
    if args.bytes:
        output.append(str(byte_count))
    if args.chars:
        output.append(str(char_count))

    print(" ".join(output))


def main():
    parser = create_parser()
    args = parser.parse_args()

    if not (args.bytes or args.chars or args.words or args.lines):
        args.bytes = args.words = args.lines = True

    if args.filename:
        if not os.path.exists(args.filename):
            print(f"Error: File '{args.filename}' does not exist.")
            return

        with open(args.filename, 'rb') as f:
            process_input(f, args)
    else:
        process_input(sys.stdin.buffer, args)


if __name__ == "__main__":
    main()

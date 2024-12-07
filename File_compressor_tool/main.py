import sys
import os
from src.main_solution import process_and_calculate


def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]

    absolute_path = os.path.abspath(filename)

    try:

        frequency = process_and_calculate(absolute_path)
        print("Character Frequencies:")
        for char, freq in frequency.items():
            print(f"{repr(char)}: {freq}")
    except Exception as e:
        print(str(e))


if __name__ == "__main__":
    main()

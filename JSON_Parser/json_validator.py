import sys
import json

def main():
    if len(sys.argv) != 2:
        print("Usage: python json_from_args.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]

    try:
        with open(filename, 'r') as file:
            input_str = file.read()

        print("Input JSON string:")
        print(input_str[1])

    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: The file '{filename}' contains invalid JSON.")
        sys.exit(1)


if __name__ == "__main__":
    main()

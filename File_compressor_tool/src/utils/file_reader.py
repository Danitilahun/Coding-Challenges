import os

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

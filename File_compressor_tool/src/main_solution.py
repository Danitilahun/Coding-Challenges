from src.utils.file_reader import process_file
from src.utils.text_utils import calculate_character_frequency

def process_and_calculate(filename: str) -> dict:
    """
    Processes a file and calculates the frequency of characters in its content.

    Args:
        filename (str): The name of the file.

    Returns:
        dict: A dictionary with character frequencies.
    """
    # Step 1: Read the file content
    content = process_file(filename)
    
    # Step 2: Calculate character frequencies
    frequency = calculate_character_frequency(content)
    
    return frequency

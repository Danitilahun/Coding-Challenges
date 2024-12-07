from collections import Counter
from typing import Dict

def calculate_character_frequency(text: str) -> Dict[str, int]:
    """
    Calculates the frequency of each character in the given text.

    Args:
        text (str): The input text.

    Returns:
        dict: A dictionary where keys are characters and values are their respective frequencies.

    Raises:
        TypeError: If the input `text` is not a string.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected input to be a string, but got {type(text).__name__} instead.")
    
    return dict(Counter(text))

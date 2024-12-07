from collections import Counter
from typing import Dict


def calculate_character_frequency(text: str) -> Dict[str,int]:
    """
    Calculates the frequency of each character in the given text.

    Args:
        text (str): The input text.

    Returns:
        dict: A dictionary where keys are characters and values are their respective frequencies.
    """
    return dict(Counter(text))

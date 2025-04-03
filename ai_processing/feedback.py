from fuzzywuzzy import fuzz
from typing import List
import json


def compare_responses(user_response: str, ideal_response: str) -> int:
    """Compares the user's response with the ideal answer using fuzzy matching."""
    return fuzz.token_set_ratio(user_response, ideal_response)

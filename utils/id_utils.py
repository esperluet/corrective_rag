import logging
from uuid import uuid4
from typing import List


def generate_list_ids(length: int) -> List[str]:
    """
    Generates a list of unique UUIDs.

    Args:
        length (int): The number of UUIDs to generate.

    Returns:
        List[str]: A list of randomly generated UUIDs as strings.

    Raises:
        ValueError: If the length is negative.
    """
    if length < 0:
        logging.error("Invalid length: Cannot generate a negative number of UUIDs.")
        raise ValueError("Length must be a non-negative integer.")

    return [str(uuid4()) for _ in range(length)]

import json
from pathlib import Path


def read_dataset_json() -> dict:
    """
    Reads a JSON file containing a dataset and returns it as a dictionary.

    Returns:
        A dictionary containing the dataset.
    """
    json_path = Path("api", "tests", "dataset.json")
    with open(json_path) as f:
        data = json.load(f)
    return data

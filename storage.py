"""Load and save student data to a JSON file."""
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "students.json")


def load_students(path=DATA_FILE):
    """Return a list of student dictionaries. Returns [] if the file is missing or broken."""
    if not os.path.exists(path):
        print("No data file yet - starting with an empty record book.")
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            print("Data file has an unexpected format - starting empty.")
            return []
        return data
    except json.JSONDecodeError:
        print("Data file is corrupted - starting empty.")
        return []
    except OSError as error:
        print(f"Could not read data file: {error}")
        return []


def save_students(records, path=DATA_FILE):
    """Write the list of student dictionaries to the JSON file. Returns True on success."""
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=4)
        return True
    except OSError as error:
        print(f"Could not save data: {error}")
        return False

from typing import List, Dict
import json
import csv
import os

def load_event_file(file_path: str) -> Dict:
    """Loads an event file (JSON, CSV, or line-delimited TXT) into a list of dictionaries.

    Args:
        file_path (str): Path to the event file.

    Returns:
        Dict: {
            "status": "success",
            "events": [...],  # List of event dictionaries
        }
        or an error message if loading fails.
    """
    if not os.path.exists(file_path):
        return {
            "status": "error",
            "error_message": f"File not found: {file_path}"
        }

    file_ext = os.path.splitext(file_path)[1].lower()

    try:
        if file_ext == ".json":
            with open(file_path, "r") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    events = [data]
                elif isinstance(data, list):
                    events = data
                else:
                    return {"status": "error", "error_message": "Unsupported JSON format"}

        elif file_ext == ".csv":
            with open(file_path, "r", newline="") as f:
                reader = csv.DictReader(f)
                events = list(reader)

        elif file_ext == ".txt":
            with open(file_path, "r") as f:
                events = [json.loads(line.strip()) for line in f if line.strip()]

        else:
            return {
                "status": "error",
                "error_message": f"Unsupported file type: {file_ext}"
            }

        return {
            "status": "success",
            "events": events
        }

    except Exception as e:
        return {
            "status": "error",
            "error_message": str(e)
        }

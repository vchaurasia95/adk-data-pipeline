import json
from typing import Dict

def validate_events(event_json: str) -> Dict:
    """Validates a JSON string of events. Returns valid and invalid events.

    Args:
        event_json (str): A JSON string representing a list of event objects.

    Returns:
        dict: A dictionary with 'valid_events' and 'invalid_events' lists.
    """
    try:
        events = json.loads(event_json)
    except json.JSONDecodeError as e:
        return {"status": "error", "error_message": f"Invalid JSON input: {str(e)}"}

    valid, invalid = [], []

    for event in events:
        if all(event.get(k) for k in ["user_id", "event_type", "timestamp"]):
            valid.append(event)
        else:
            invalid.append(event)

    return {
        "status": "success",
        "valid_events": valid,
        "invalid_events": invalid
    }
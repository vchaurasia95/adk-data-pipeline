import hashlib
import json
from typing import Dict

def deduplicate_events(event_json: str) -> Dict:
    """Accepts a JSON string of event list and returns deduplicated results."""
    try:
        event_list = json.loads(event_json)
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Invalid JSON input: {str(e)}"
        }

    seen = set()
    deduped = []

    for event in event_list:
        event_str = json.dumps(event, sort_keys=True)
        event_hash = hashlib.md5(event_str.encode()).hexdigest()
        if event_hash not in seen:
            deduped.append(event)
            seen.add(event_hash)

    return {
        "status": "success",
        "deduplicated_events": deduped,
        "summary": f"{len(event_list) - len(deduped)} duplicates removed"
    }

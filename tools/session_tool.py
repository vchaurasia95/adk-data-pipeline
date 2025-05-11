import json
from typing import Dict
from datetime import datetime, timedelta

def assign_sessions(event_json: str, session_gap_minutes: int = 30) -> Dict:
    """
    Assigns session IDs to events per user based on time gaps.
    Uses user_id as session_id to keep schema simple.

    Args:
        event_json (str): JSON string representing a list of event records.
        session_gap_minutes (int): Gap threshold to start new session.

    Returns:
        Dict: sessionized events with summary or error.
    """
    try:
        event_list = json.loads(event_json)
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Invalid JSON input: {str(e)}"
        }

    event_list.sort(key=lambda x: (x['user_id'], x['timestamp']))
    sessions = []
    last_timestamp = None
    last_user = None
    gap = timedelta(minutes=session_gap_minutes)

    for event in event_list:
        user_id = event['user_id']
        ts = datetime.fromisoformat(event['timestamp'].replace("Z", "+00:00"))

        is_new_session = (
            last_user != user_id or
            (last_timestamp and ts - last_timestamp > gap)
        )

        if is_new_session:
            session_id = user_id  # use user_id as session_id

        event['session_id'] = session_id
        sessions.append(event)
        last_timestamp = ts
        last_user = user_id

    return {
        "status": "success",
        "sessionized_events": sessions,
        "summary": f"{len(sessions)} events grouped into sessions"
    }

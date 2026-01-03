import json
import os
from datetime import datetime
from typing import List, Dict

EVENT_LOG_DIR = "knowledge_events"


def _ensure_dir():
    os.makedirs(EVENT_LOG_DIR, exist_ok=True)


def log_event(event_type: str, payload: Dict):
    """
    Stores an immutable event record.
    Used for compliance, audits, and traceability.
    """
    _ensure_dir()

    event = {
        "event_type": event_type,
        "payload": payload,
        "timestamp": datetime.utcnow().isoformat(),
    }

    filename = f"{EVENT_LOG_DIR}/{datetime.utcnow().timestamp()}.json"
    with open(filename, "w") as f:
        json.dump(event, f, indent=2)


def get_event_log() -> List[Dict]:
    """
    Returns all logged events (read-only).
    Used by Compliance API.
    """
    _ensure_dir()

    events = []
    for file in sorted(os.listdir(EVENT_LOG_DIR)):
        path = os.path.join(EVENT_LOG_DIR, file)
        if path.endswith(".json"):
            with open(path) as f:
                events.append(json.load(f))

    return events
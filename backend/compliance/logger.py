import json
from pathlib import Path
from backend.compliance.models import ComplianceEvent

LOG_DIR = Path("compliance_logs")
LOG_DIR.mkdir(exist_ok=True)


def log_compliance_event(event: ComplianceEvent):
    file_path = LOG_DIR / f"{event.event_id}.json"
    with open(file_path, "w") as f:
        json.dump(event.dict(), f, indent=2, default=str)
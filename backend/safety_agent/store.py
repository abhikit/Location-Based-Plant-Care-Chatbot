import json
import uuid
from pathlib import Path
from backend.safety_agent.models import SafetyAssessment

STORE_PATH = Path("safety_audits")
STORE_PATH.mkdir(exist_ok=True)


def store_safety_assessment(assessment: SafetyAssessment) -> str:
    audit_id = str(uuid.uuid4())
    file_path = STORE_PATH / f"{audit_id}.json"

    with open(file_path, "w") as f:
        json.dump(assessment.dict(), f, indent=2, default=str)

    return audit_id
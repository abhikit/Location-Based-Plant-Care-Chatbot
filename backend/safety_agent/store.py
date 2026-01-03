import json
from pathlib import Path
from typing import List

from backend.safety_agent.models import SafetyAssessment

# Directory where audits are stored
AUDIT_DIR = Path("safety_audits")
AUDIT_DIR.mkdir(exist_ok=True)


def store_safety_audit(assessment: SafetyAssessment) -> None:
    """
    Persist a safety assessment to disk.
    """
    path = AUDIT_DIR / f"{assessment.id}.json"
    with open(path, "w") as f:
        json.dump(assessment.dict(), f, indent=2)


def get_safety_audits() -> List[SafetyAssessment]:
    """
    Load all safety audits for compliance dashboard.
    """
    audits: List[SafetyAssessment] = []

    for file in AUDIT_DIR.glob("*.json"):
        with open(file) as f:
            data = json.load(f)
            audits.append(SafetyAssessment(**data))

    return audits
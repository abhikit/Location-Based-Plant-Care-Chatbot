from typing import List
from uuid import uuid4

from backend.safety_agent.models import SafetyAssessment


def assess_risk(answer: str) -> SafetyAssessment:
    """
    Lightweight rule-based safety assessment.
    This agent NEVER changes the answer.
    """

    flags: List[str] = []
    risk_level = "low"

    lowered = answer.lower()

    # Basic heuristics (extend later via policy engine)
    if any(word in lowered for word in ["poison", "toxic", "kill", "medicine", "dosage"]):
        risk_level = "medium"
        flags.append("potentially_harmful_advice")

    if any(word in lowered for word in ["consume", "eat", "drink"]):
        risk_level = "high"
        flags.append("human_consumption_risk")

    return SafetyAssessment(
        id=str(uuid4()),
        risk_level=risk_level,
        flags=flags,
        disclaimer_added=False,
    )
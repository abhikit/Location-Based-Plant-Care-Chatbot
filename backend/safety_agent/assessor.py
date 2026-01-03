from backend.safety_agent.models import SafetyAssessment
from backend.safety_agent.policy import apply_policy_rules


def assess_risk(
    session_id: str,
    user_question: str,
    answer: str,
) -> SafetyAssessment:
    policy_flags = apply_policy_rules(answer)

    if not policy_flags:
        return SafetyAssessment(
            session_id=session_id,
            risk_level="low",
            risk_categories=[],
            explanation="No safety risks detected."
        )

    risk_level = "medium"
    if "toxic_chemical" in policy_flags:
        risk_level = "high"

    return SafetyAssessment(
        session_id=session_id,
        risk_level=risk_level,
        risk_categories=policy_flags,
        explanation=(
            "Potential safety concerns detected in generated answer. "
            "Human review recommended."
        ),
        recommendation="Add disclaimers or restrict advice scope."
    )
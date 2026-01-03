# backend/knowledge/risk_safety_agent.py

from typing import List, Literal
from pydantic import BaseModel, Field

from backend.knowledge.schema import KnowledgeChunk


class RiskAssessment(BaseModel):
    """
    Output of the Risk & Safety Agent.

    This object NEVER modifies knowledge.
    It only evaluates risk.
    """

    risk_level: Literal["low", "medium", "high"] = Field(
        ...,
        description="Overall safety risk of the knowledge"
    )

    reasons: List[str] = Field(
        ...,
        description="Why this risk level was assigned"
    )

    requires_human_approval: bool = Field(
        ...,
        description="Whether human review is mandatory"
    )


def assess_risk(knowledge: KnowledgeChunk) -> RiskAssessment:
    """
    Rule-based risk & safety evaluation.

    NO LLM USED HERE (by design).
    Deterministic and auditable.
    """

    risk_level = "low"
    reasons: List[str] = []
    requires_human_approval = False

    # ------------------------------------
    # High-risk indicators
    # ------------------------------------
    dangerous_keywords = [
        "chemical",
        "pesticide",
        "fungicide",
        "insecticide",
        "spray",
        "dose",
        "concentration",
        "mix",
        "apply directly",
        "toxic",
    ]

    for action in knowledge.recommended_actions:
        lower_action = action.lower()
        for keyword in dangerous_keywords:
            if keyword in lower_action:
                risk_level = "high"
                requires_human_approval = True
                reasons.append(
                    f"Action contains potentially dangerous instruction: '{keyword}'"
                )

    # ------------------------------------
    # Medium-risk indicators
    # ------------------------------------
    if knowledge.category in ["disease", "pest", "nutrition"]:
        if risk_level != "high":
            risk_level = "medium"
            requires_human_approval = True
            reasons.append(
                f"Category '{knowledge.category}' requires expert validation"
            )

    # ------------------------------------
    # Confidence-based risk
    # ------------------------------------
    if knowledge.confidence == "low":
        risk_level = "medium"
        requires_human_approval = True
        reasons.append("Knowledge confidence is low")

    # ------------------------------------
    # Final fallback
    # ------------------------------------
    if not reasons:
        reasons.append("No safety risks detected")

    return RiskAssessment(
        risk_level=risk_level,
        reasons=reasons,
        requires_human_approval=requires_human_approval,
    )
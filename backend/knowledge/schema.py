# backend/knowledge/schema.py

from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class KnowledgeChunk(BaseModel):
    """
    Canonical representation of plant knowledge.

    ALL agents must output knowledge ONLY in this format.
    This schema is immutable once approved.
    """

    # ----------------------------
    # Core Identification
    # ----------------------------
    plant: str = Field(
        ...,
        description="Plant name (e.g., Rose, Tomato, Basil)"
    )

    category: Literal[
        "watering",
        "soil",
        "nutrition",
        "disease",
        "pest",
        "environment_stress",
        "seasonal_care",
    ] = Field(
        ...,
        description="Primary category of the knowledge"
    )

    # ----------------------------
    # Condition & Symptoms
    # ----------------------------
    condition: Optional[str] = Field(
        None,
        description="Specific condition or issue (e.g., Nitrogen deficiency)"
    )

    symptoms: List[str] = Field(
        ...,
        description="Observable symptoms in the plant"
    )

    causes: List[str] = Field(
        ...,
        description="Underlying causes of the condition"
    )

    # ----------------------------
    # Recommended Actions
    # ----------------------------
    recommended_actions: List[str] = Field(
        ...,
        description="Safe, actionable care recommendations"
    )

    # ----------------------------
    # Contextual Applicability
    # ----------------------------
    applicable_climate: Optional[str] = Field(
        None,
        description="Climate context (e.g., hot-dry, tropical, temperate)"
    )

    applicable_season: Optional[str] = Field(
        None,
        description="Season where this knowledge applies (e.g., summer, winter)"
    )

    # ----------------------------
    # Governance & Trust
    # ----------------------------
    confidence: Literal[
        "low",
        "medium",
        "high"
    ] = Field(
        ...,
        description="Confidence level of the knowledge"
    )

    source: Literal[
        "expert",
        "derived",
        "user_observation"
    ] = Field(
        ...,
        description="Origin of the knowledge"
    )

    # ----------------------------
    # Metadata (internal use)
    # ----------------------------
    notes: Optional[str] = Field(
        None,
        description="Internal notes for reviewers (not shown to users)"
    )

    version: int = Field(
        default=1,
        description="Schema version for future migrations"
    )
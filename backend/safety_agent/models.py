from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class SafetyAssessment(BaseModel):
    """
    Represents a safety evaluation for an answer.
    Stored for compliance & audits.
    """

    id: str
    risk_level: str = Field(
        description="low | medium | high"
    )
    flags: List[str] = Field(
        default_factory=list,
        description="Detected safety concerns"
    )
    disclaimer_added: bool = False
    assessed_at: datetime = Field(
        default_factory=datetime.utcnow
    )
    assessed_by: str = "safety_agent"
from pydantic import BaseModel
from typing import List, Literal, Optional
from datetime import datetime


class SafetyAssessment(BaseModel):
    session_id: str
    risk_level: Literal["low", "medium", "high"]
    risk_categories: List[str]
    explanation: str
    recommendation: Optional[str] = None
    timestamp: datetime = datetime.utcnow()
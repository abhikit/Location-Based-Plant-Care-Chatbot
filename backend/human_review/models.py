from pydantic import BaseModel
from typing import Optional, Literal, Dict
from datetime import datetime


class HumanReviewDecision(BaseModel):
    proposal_id: str
    decision: Literal["approve", "reject", "edit"]
    reviewer: str
    comments: Optional[str] = None
    edited_content: Optional[str] = None
    timestamp: datetime = datetime.utcnow()
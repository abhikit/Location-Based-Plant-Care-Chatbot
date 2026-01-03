from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime
from uuid import uuid4

from backend.knowledge.schema import KnowledgeChunk
from backend.knowledge.risk_safety_agent import RiskAssessment


class ApprovalStatus(BaseModel):
    id: str
    knowledge: KnowledgeChunk
    risk: RiskAssessment
    status: Literal["pending", "approved", "rejected"]
    reviewer_comment: Optional[str]
    created_at: datetime
    reviewed_at: Optional[datetime]


def create_pending_approval(
    knowledge: KnowledgeChunk,
    risk: RiskAssessment
) -> ApprovalStatus:
    return ApprovalStatus(
        id=str(uuid4()),
        knowledge=knowledge,
        risk=risk,
        status="pending",
        reviewer_comment=None,
        created_at=datetime.utcnow(),
        reviewed_at=None,
    )
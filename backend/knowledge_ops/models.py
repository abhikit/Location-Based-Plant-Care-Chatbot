from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime
from backend.knowledge_ops.states import KnowledgeState


class KnowledgeEvent(BaseModel):
    event_id: str
    session_id: str
    question: str
    detected_at: datetime
    reason: str
    state: KnowledgeState = KnowledgeState.DETECTED
    metadata: Dict = Field(default_factory=dict)


class KnowledgeProposal(BaseModel):
    proposal_id: str
    event_id: str
    title: str
    proposed_content: str
    confidence: float
    created_at: datetime
    state: KnowledgeState = KnowledgeState.PROPOSED
    reviewer_notes: Optional[str] = None
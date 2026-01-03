from typing import List, Literal
from pydantic import BaseModel
from datetime import datetime
import uuid


class KnowledgeApprovalItem(BaseModel):
    id: str
    created_at: datetime
    status: Literal["pending", "approved", "rejected"]

    user_question: str
    missing_concepts: List[str]
    suggested_sources: List[str]
    priority: Literal["low", "medium", "high"]
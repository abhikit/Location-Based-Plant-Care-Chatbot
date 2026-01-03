from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
import uuid


class ComplianceEvent(BaseModel):
    event_id: str = uuid.uuid4().hex
    timestamp: datetime = datetime.utcnow()

    session_id: str
    user_question: str

    answer_source: str
    input_mode: str

    used_rag: bool
    used_environment: bool
    used_vision: bool

    risk_level: Optional[str]
    disclaimer_injected: bool

    knowledge_proposal_id: Optional[str]

    metadata: Dict[str, Any] = {}
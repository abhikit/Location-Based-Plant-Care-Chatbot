from typing import Optional, Dict, Any
from pydantic import BaseModel


class AgentExecutionResult(BaseModel):
    answer: Optional[str] = None
    environment_summary: Optional[str] = None
    vision_summary: Optional[str] = None
    knowledge_gap_detected: bool = False
    knowledge_proposal: Optional[Dict[str, Any]] = None
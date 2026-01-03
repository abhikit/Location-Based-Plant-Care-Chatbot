from typing import List, Literal
from pydantic import BaseModel


class KnowledgeProposal(BaseModel):
    should_enrich: bool
    missing_concepts: List[str]
    suggested_sources: List[str]
    priority: Literal["low", "medium", "high"]
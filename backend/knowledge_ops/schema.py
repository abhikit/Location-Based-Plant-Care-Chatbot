from typing import List, Dict
from datetime import datetime
from pydantic import BaseModel, Field


class PlantKnowledgeEntry(BaseModel):
    plant_name: str
    symptom: str

    possible_causes: List[str]

    recommended_actions: List[Dict]  # {action: str, priority: int}

    sources: List[str]

    confidence: Dict  # {score: float, rationale: str}

    approved: bool = False

    created_by: str  # agent | human

    created_at: datetime = Field(default_factory=datetime.utcnow)
from datetime import datetime
from typing import List
from backend.knowledge_ops.schema import PlantKnowledgeEntry


def compute_staleness_days(entry: PlantKnowledgeEntry) -> int:
    created_at = entry.created_at or datetime.utcnow()
    return (datetime.utcnow() - created_at).days


def compute_confidence_decay(entry: PlantKnowledgeEntry) -> float:
    """
    Simple decay: 2% confidence loss per month
    """
    days_old = compute_staleness_days(entry)
    decay = (days_old / 30) * 0.02
    return max(entry.confidence["score"] - decay, 0.1)


def duplication_score(
    entry: PlantKnowledgeEntry,
    corpus: List[PlantKnowledgeEntry],
) -> float:
    """
    Measures how many similar symptom entries already exist
    """
    matches = [
        e for e in corpus
        if e.plant_name == entry.plant_name
        and e.symptom.lower() == entry.symptom.lower()
    ]

    if not matches:
        return 0.0

    return min(len(matches) / 5, 1.0)
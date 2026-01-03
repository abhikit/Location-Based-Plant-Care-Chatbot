from typing import List
from backend.knowledge_ops.schema import PlantKnowledgeEntry
from backend.knowledge_ops.metrics import (
    compute_staleness_days,
    compute_confidence_decay,
    duplication_score,
)
from backend.knowledge_ops.conflict_detector import detect_conflicts


def knowledge_quality_report(
    entry: PlantKnowledgeEntry,
    corpus: List[PlantKnowledgeEntry],
) -> dict:
    return {
        "plant": entry.plant_name,
        "symptom": entry.symptom,
        "approved": entry.approved,
        "staleness_days": compute_staleness_days(entry),
        "confidence_original": entry.confidence["score"],
        "confidence_decayed": compute_confidence_decay(entry),
        "duplication_score": duplication_score(entry, corpus),
        "conflict_detected": detect_conflicts(entry, corpus),
        "review_required": (
            not entry.approved
            or compute_confidence_decay(entry) < 0.4
            or detect_conflicts(entry, corpus)
        ),
    }
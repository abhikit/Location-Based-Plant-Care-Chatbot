from typing import List
from backend.knowledge_ops.schema import PlantKnowledgeEntry


CONFLICTING_ACTIONS = [
    ("increase watering", "reduce watering"),
    ("move to shade", "move to full sun"),
]


def detect_conflicts(
    entry: PlantKnowledgeEntry,
    corpus: List[PlantKnowledgeEntry],
) -> bool:
    entry_actions = {a["action"].lower() for a in entry.recommended_actions}

    for existing in corpus:
        if existing.plant_name != entry.plant_name:
            continue

        existing_actions = {
            a["action"].lower()
            for a in existing.recommended_actions
        }

        for a, b in CONFLICTING_ACTIONS:
            if (a in entry_actions and b in existing_actions) or \
               (b in entry_actions and a in existing_actions):
                return True

    return False
import json
from pathlib import Path
from typing import List
from backend.knowledge_ops.schema import PlantKnowledgeEntry

STORE_PATH = Path("data/knowledge_review_queue.json")
STORE_PATH.parent.mkdir(exist_ok=True)


def _load() -> List[dict]:
    if not STORE_PATH.exists():
        return []
    return json.loads(STORE_PATH.read_text())


def _save(data: List[dict]):
    STORE_PATH.write_text(json.dumps(data, indent=2, default=str))


def add_proposal(entry: PlantKnowledgeEntry) -> str:
    data = _load()
    record = entry.dict()
    record["id"] = f"kp_{len(data)+1}"
    data.append(record)
    _save(data)
    return record["id"]


def list_pending() -> List[dict]:
    return [r for r in _load() if not r.get("approved")]


def update_status(proposal_id: str, approved: bool):
    data = _load()
    for r in data:
        if r["id"] == proposal_id:
            r["approved"] = approved
    _save(data)


def get_by_id(proposal_id: str) -> dict | None:
    for r in _load():
        if r["id"] == proposal_id:
            return r
    return None
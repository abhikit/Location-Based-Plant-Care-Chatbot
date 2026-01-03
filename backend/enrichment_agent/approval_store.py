from typing import Dict, List
import uuid

# In-memory store (Phase-2)
# Later → DB / Admin Panel
PROPOSAL_STORE: Dict[str, Dict] = {}


def store_proposal(proposal: Dict) -> str:
    """
    Save a knowledge proposal for human review.
    """
    proposal_id = str(uuid.uuid4())
    proposal["id"] = proposal_id
    proposal["status"] = "PENDING"
    PROPOSAL_STORE[proposal_id] = proposal
    return proposal_id


def list_pending_proposals() -> List[Dict]:
    return [
        p for p in PROPOSAL_STORE.values()
        if p["status"] == "PENDING"
    ]


def update_proposal_status(proposal_id: str, status: str):
    if proposal_id in PROPOSAL_STORE:
        PROPOSAL_STORE[proposal_id]["status"] = status
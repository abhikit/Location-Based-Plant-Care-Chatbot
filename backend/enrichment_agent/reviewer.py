from fastapi import APIRouter, HTTPException
from backend.enrichment_agent.approval_store import (
    list_pending_proposals,
    update_proposal_status,
)

router = APIRouter(prefix="/admin", tags=["Human Review"])


@router.get("/proposals")
def get_pending_proposals():
    """
    Human reviews pending proposals.
    """
    return list_pending_proposals()


@router.post("/proposals/{proposal_id}/approve")
def approve_proposal(proposal_id: str):
    update_proposal_status(proposal_id, "APPROVED")
    return {"status": "approved", "id": proposal_id}


@router.post("/proposals/{proposal_id}/reject")
def reject_proposal(proposal_id: str):
    update_proposal_status(proposal_id, "REJECTED")
    return {"status": "rejected", "id": proposal_id}
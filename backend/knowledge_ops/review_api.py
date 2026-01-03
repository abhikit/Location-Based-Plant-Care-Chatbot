from fastapi import APIRouter, HTTPException
from backend.knowledge_ops.approval_store import (
    list_pending,
    update_status,
    get_by_id,
)
from backend.knowledge_ops.schema import PlantKnowledgeEntry
from backend.knowledge_ops.promoter import promote_to_knowledge_base

router = APIRouter(prefix="/review", tags=["Knowledge Review"])


@router.get("/pending")
def pending_proposals():
    return list_pending()


@router.post("/approve/{proposal_id}")
def approve_proposal(proposal_id: str):
    record = get_by_id(proposal_id)
    if not record:
        raise HTTPException(status_code=404, detail="Proposal not found")

    update_status(proposal_id, approved=True)
    promote_to_knowledge_base(PlantKnowledgeEntry(**record))
    return {"status": "approved", "id": proposal_id}


@router.post("/reject/{proposal_id}")
def reject_proposal(proposal_id: str):
    if not get_by_id(proposal_id):
        raise HTTPException(status_code=404, detail="Proposal not found")

    update_status(proposal_id, approved=False)
    return {"status": "rejected", "id": proposal_id}
from fastapi import APIRouter
from backend.enrichment_agent.approval_store import load_queue

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/approval-queue")
def get_approval_queue():
    return load_queue()
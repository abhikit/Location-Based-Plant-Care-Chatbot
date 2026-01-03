from fastapi import APIRouter, HTTPException
from typing import List

from backend.approval.store import get_pending
from backend.approval.service import approve, reject
from backend.approval.models import ApprovalStatus

router = APIRouter(prefix="/approvals", tags=["Human Approval"])


@router.get("/pending", response_model=List[ApprovalStatus])
def list_pending():
    return get_pending()


@router.post("/{approval_id}/approve")
def approve_knowledge(approval_id: str, comment: str | None = None):
    try:
        approve(approval_id, comment)
        return {"status": "approved"}
    except KeyError:
        raise HTTPException(404, "Approval not found")


@router.post("/{approval_id}/reject")
def reject_knowledge(approval_id: str, comment: str):
    try:
        reject(approval_id, comment)
        return {"status": "rejected"}
    except KeyError:
        raise HTTPException(404, "Approval not found")
from datetime import datetime

from backend.approval.models import (
    create_pending_approval,
    ApprovalStatus,
)
from backend.approval.store import save_approval, get_by_id, update
from backend.knowledge.kb_writer import add_to_knowledge_base


def submit_for_approval(knowledge, risk) -> ApprovalStatus:
    approval = create_pending_approval(knowledge, risk)
    save_approval(approval)
    return approval


def approve(approval_id: str, comment: str | None = None):
    approval = get_by_id(approval_id)
    approval.status = "approved"
    approval.reviewer_comment = comment
    approval.reviewed_at = datetime.utcnow()

    add_to_knowledge_base(approval.knowledge)
    update(approval)


def reject(approval_id: str, comment: str):
    approval = get_by_id(approval_id)
    approval.status = "rejected"
    approval.reviewer_comment = comment
    approval.reviewed_at = datetime.utcnow()
    update(approval)
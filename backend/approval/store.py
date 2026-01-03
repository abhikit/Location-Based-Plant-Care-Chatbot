from typing import Dict, List
from .models import ApprovalStatus

_APPROVAL_STORE: Dict[str, ApprovalStatus] = {}


def save_approval(item: ApprovalStatus):
    _APPROVAL_STORE[item.id] = item


def get_pending() -> List[ApprovalStatus]:
    return [
        a for a in _APPROVAL_STORE.values()
        if a.status == "pending"
    ]


def get_by_id(approval_id: str) -> ApprovalStatus:
    return _APPROVAL_STORE[approval_id]


def update(item: ApprovalStatus):
    _APPROVAL_STORE[item.id] = item
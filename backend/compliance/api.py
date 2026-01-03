from fastapi import APIRouter
from backend.knowledge_ops.event_logger import get_event_log
from backend.safety_agent.store import get_safety_audits

router = APIRouter(prefix="/compliance", tags=["Compliance"])


@router.get("/events")
def list_events():
    """
    Returns all system events:
    - knowledge proposals
    - approvals
    - promotions
    """
    return get_event_log()


@router.get("/safety-audits")
def list_safety_audits():
    """
    Returns all safety assessments & disclaimer decisions
    """
    return get_safety_audits()
import uuid
from datetime import datetime
from backend.knowledge_ops.models import KnowledgeEvent


_EVENT_LOG: list[KnowledgeEvent] = []


def log_knowledge_event(
    session_id: str,
    question: str,
    reason: str,
    metadata: dict | None = None,
) -> KnowledgeEvent:
    event = KnowledgeEvent(
        event_id=str(uuid.uuid4()),
        session_id=session_id,
        question=question,
        detected_at=datetime.utcnow(),
        reason=reason,
        metadata=metadata or {},
    )

    _EVENT_LOG.append(event)
    return event


def list_events() -> list[KnowledgeEvent]:
    return _EVENT_LOG
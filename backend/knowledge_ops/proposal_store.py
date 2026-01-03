import uuid
from datetime import datetime
from backend.knowledge_ops.models import KnowledgeProposal


_PROPOSALS: dict[str, KnowledgeProposal] = {}


def store_proposal(
    event_id: str,
    title: str,
    proposed_content: str,
    confidence: float,
) -> KnowledgeProposal:
    proposal = KnowledgeProposal(
        proposal_id=str(uuid.uuid4()),
        event_id=event_id,
        title=title,
        proposed_content=proposed_content,
        confidence=confidence,
        created_at=datetime.utcnow(),
    )

    _PROPOSALS[proposal.proposal_id] = proposal
    return proposal


def get_proposal(proposal_id: str) -> KnowledgeProposal | None:
    return _PROPOSALS.get(proposal_id)


def list_proposals() -> list[KnowledgeProposal]:
    return list(_PROPOSALS.values())
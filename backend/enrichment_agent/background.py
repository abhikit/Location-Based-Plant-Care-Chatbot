from backend.enrichment_agent.detector import detect_knowledge_gap
from backend.enrichment_agent.proposer import propose_knowledge_enrichment
from backend.enrichment_agent.approval_store import store_proposal


def run_async_enrichment(
    *,
    user_question: str,
    rag_chunks: list[str],
    llm_answer: str,
    environment_summary: str | None,
    vision_summary: str | None,
):
    """
    Runs enrichment agents asynchronously.

    IMPORTANT:
    - Never blocks user response
    - Safe to fail silently
    - Read-only on existing knowledge
    """

    try:
        gap_detected = detect_knowledge_gap(
            user_question=user_question,
            rag_chunks=rag_chunks,
            llm_answer=llm_answer,
            environment_summary=environment_summary,
            vision_summary=vision_summary,
        )

        if not gap_detected:
            return

        proposal = propose_knowledge_enrichment(
            user_question=user_question,
            rag_chunks=rag_chunks,
            llm_answer=llm_answer,
            environment_summary=environment_summary,
            vision_summary=vision_summary,
        )

        if proposal:
            store_proposal(proposal)

    except Exception as e:
        # Background agents must NEVER crash the system
        print(f"[Async Enrichment Error] {e}")
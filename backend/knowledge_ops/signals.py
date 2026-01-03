from typing import Dict


def extract_quality_signals(
    *,
    user_question: str,
    rag_chunks: list[str],
    llm_answer: str,
    environment_summary: str | None,
    vision_summary: str | None,
) -> Dict:
    """
    Extract raw signals used for quality scoring.
    NO LLM CALLS.
    """

    signals = {
        "rag_chunk_count": len(rag_chunks),
        "answer_length": len(llm_answer),
        "mentions_environment": bool(environment_summary and environment_summary in llm_answer),
        "mentions_vision": bool(vision_summary and vision_summary in llm_answer),
        "question_length": len(user_question),
        "rag_coverage_ratio": min(len(rag_chunks) / 3, 1.0),
    }

    return signals
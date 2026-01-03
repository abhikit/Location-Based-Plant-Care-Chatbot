from typing import List, Optional


def detect_knowledge_gap(
    user_question: str,
    rag_chunks: List[str],
    llm_answer: str,
    environment_summary: Optional[str] = None,
    vision_summary: Optional[str] = None,
) -> bool:
    """
    Detects whether the current knowledge base is insufficient.

    Returns:
        True  -> Knowledge gap detected
        False -> Knowledge sufficient
    """

    # Very simple, safe heuristic (Phase-2B)
    # You can evolve this later

    if not rag_chunks:
        return True

    # If answer contains uncertainty signals
    uncertainty_markers = [
        "not enough information",
        "cannot determine",
        "insufficient data",
        "may depend",
    ]

    lower_answer = llm_answer.lower()

    for marker in uncertainty_markers:
        if marker in lower_answer:
            return True

    return False
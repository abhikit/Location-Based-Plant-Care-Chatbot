from typing import Dict


def score_grounding(signals: Dict) -> float:
    """
    Measures how well the answer is grounded in RAG.
    """
    return min(signals["rag_chunk_count"] / 3, 1.0)


def score_completeness(signals: Dict) -> float:
    """
    Measures completeness relative to question complexity.
    """
    if signals["question_length"] == 0:
        return 0.0
    return min(signals["answer_length"] / (signals["question_length"] * 3), 1.0)


def score_context_usage(signals: Dict) -> float:
    """
    Rewards use of environment / vision when available.
    """
    score = 0.0
    if signals["mentions_environment"]:
        score += 0.5
    if signals["mentions_vision"]:
        score += 0.5
    return score


def aggregate_quality_score(signals: Dict) -> Dict:
    """
    Final quality metrics used by Knowledge Ops.
    """
    grounding = score_grounding(signals)
    completeness = score_completeness(signals)
    context = score_context_usage(signals)

    final_score = round(
        (0.5 * grounding) + (0.3 * completeness) + (0.2 * context),
        3
    )

    return {
        "grounding_score": grounding,
        "completeness_score": completeness,
        "context_score": context,
        "final_quality_score": final_score,
    }
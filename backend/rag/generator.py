from typing import List, Dict, Optional
import os
from openai import OpenAI

# --------------------------------------------------
# OpenAI client (ONLY place LLM is used)
# --------------------------------------------------
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_answer(
    question: str,
    context_chunks: List[str],
    memory: List[Dict[str, str]],
    environment_summary: Optional[str] = None,
    vision_summary: Optional[str] = None,
) -> str:
    """
    Generate a grounded plant-care answer using:
    - RAG context (authoritative knowledge)
    - Conversation memory (supporting context)
    - Environment signals (modifier)
    - Vision signals (modifier)

    HARD RULES:
    - NEVER hallucinate
    - NEVER answer outside provided knowledge
    - If KB is insufficient → explicitly say so
    """

    # --------------------------------------------------
    # Build authoritative knowledge context
    # --------------------------------------------------
    context_text = "\n\n".join(context_chunks)

    system_prompt = (
        "You are a plant care assistant.\n"
        "You MUST answer using ONLY the provided plant knowledge.\n"
        "Conversation history is for context only.\n"
        "If the knowledge base does not contain enough information, "
        "you MUST clearly say that you do not have enough information.\n\n"
        "=== PLANT KNOWLEDGE BASE ===\n"
        f"{context_text}\n"
        "=== END PLANT KNOWLEDGE BASE ==="
    )

    # --------------------------------------------------
    # Environment context (modifier, not knowledge)
    # --------------------------------------------------
    if environment_summary:
        system_prompt += (
            "\n\n=== ENVIRONMENT CONTEXT ===\n"
            f"{environment_summary}\n"
            "You MUST explicitly explain how these conditions "
            "affect plant care.\n"
            "=== END ENVIRONMENT CONTEXT ==="
        )

    # --------------------------------------------------
    # Vision context (modifier, not knowledge)
    # --------------------------------------------------
    if vision_summary:
        system_prompt += (
            "\n\n=== VISION CONTEXT ===\n"
            f"{vision_summary}\n"
            "Use visual observations ONLY if they are supported "
            "by the plant knowledge base.\n"
            "=== END VISION CONTEXT ==="
        )

    # --------------------------------------------------
    # Assemble messages
    # --------------------------------------------------
    messages = [{"role": "system", "content": system_prompt}]

    # Add conversation memory (supporting only)
    for msg in memory:
        messages.append(msg)

    # Add user question
    messages.append({"role": "user", "content": question})

    # --------------------------------------------------
    # Call LLM (single controlled entry point)
    # --------------------------------------------------
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.2,
    )

    return response.choices[0].message.content.strip()
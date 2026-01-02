import os
from dotenv import load_dotenv
from openai import OpenAI
from typing import List, Dict, Optional

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_answer(
    question: str,
    context_chunks: List[str],
    memory: List[Dict[str, str]],
    environment_summary: Optional[str] = None,
    vision_summary: Optional[str] = None
) -> str:
    """
    Generate a grounded answer using:
    - RAG context (authoritative)
    - Conversation memory (supporting)
    - Environment summary (modifier)
    - Vision summary (symptom signal only)
    """

    context_text = "\n\n".join(context_chunks)

    system_prompt = (
        "You are a plant care assistant.\n"
        "Answer the user's question using ONLY the plant knowledge provided.\n"
        "Conversation history is for context only.\n"
        "If the knowledge is insufficient, say you do not have enough information.\n\n"
        "=== PLANT KNOWLEDGE BASE ===\n"
        f"{context_text}\n"
        "=== END PLANT KNOWLEDGE BASE ==="
    )

    if environment_summary:
        system_prompt += (
            "\n\n=== ENVIRONMENT CONTEXT ===\n"
            f"{environment_summary}\n"
            "You MUST explicitly incorporate the environment context "
            "(temperature, humidity, AQI, pollution) into your answer. "
            "Explain how these conditions affect plant care.\n"
            "=== END ENVIRONMENT CONTEXT ==="
        )

    if vision_summary:
        system_prompt += (
            "\n\n=== VISUAL OBSERVATIONS ===\n"
            f"{vision_summary}\n"
            "These observations describe visible plant symptoms only. "
            "Use them to better understand the plant condition, "
            "but do NOT invent causes or treatments not supported by the plant knowledge base.\n"
            "=== END VISUAL OBSERVATIONS ==="
        )

    messages = [{"role": "system", "content": system_prompt}]

    # Conversation memory (supporting only)
    for msg in memory:
        messages.append(msg)

    messages.append({"role": "user", "content": question})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.2
    )

    return response.choices[0].message.content.strip()
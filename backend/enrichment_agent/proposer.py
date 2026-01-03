from typing import List, Optional, Dict
import os

def propose_knowledge_enrichment(
    user_question: str,
    rag_chunks: List[str],
    llm_answer: str,
    environment_summary: Optional[str] = None,
    vision_summary: Optional[str] = None,
) -> Optional[Dict]:
    """
    Step-2C: Knowledge Proposal Agent

    Purpose:
    - Suggest missing knowledge areas
    - NEVER block chat
    - NEVER invent facts
    - Safe if OpenAI key is missing
    """

    # 🔒 Safety: Do nothing if no OpenAI key
    if not os.getenv("OPENAI_API_KEY"):
        return None

    try:
        from openai import OpenAI
        client = OpenAI()

        prompt = f"""
You are a knowledge curator.

User question:
{user_question}

Answer given:
{llm_answer}

Environment:
{environment_summary}

Vision:
{vision_summary}

RAG Context:
{rag_chunks}

Task:
Identify if the knowledge base is missing structured information.
Respond ONLY in JSON with keys:
plant_name, category, missing_aspect, confidence

If no gap, return null.
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a knowledge gap detector."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.0,
        )

        content = response.choices[0].message.content.strip()

        if content.lower() == "null":
            return None

        return eval(content)  # trusted internal agent output

    except Exception:
        # 🔕 Silent failure by design
        return None
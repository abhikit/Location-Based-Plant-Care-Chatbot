from openai import OpenAI
import json
from backend.agent_router.models import ToolDecision

client = OpenAI()


def decide_tools(
    question: str,
    has_image: bool,
    has_location: bool,
) -> ToolDecision:
    """
    Decide which tools should run.
    This agent NEVER answers user questions.
    """

    system_prompt = """
You are a tool-routing agent for a plant care system.

Rules:
- You NEVER answer user questions.
- You ONLY decide which tools should run.
- RAG is ALWAYS required.
- Vision ONLY if image is provided.
- Environment ONLY if location is available.
- Knowledge proposal ONLY if question may exceed KB.

Return STRICT JSON with this schema:

{
  "use_rag": boolean,
  "use_vision": boolean,
  "use_environment": boolean,
  "may_need_knowledge_enrichment": boolean,
  "explanation": string
}
"""

    user_prompt = f"""
User question:
{question}

Image uploaded: {has_image}
Location available: {has_location}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0,
    )

    # --------------------------------------------------
    # 🔐 SAFE PARSING (NO TRUST IN LLM)
    # --------------------------------------------------
    raw_json = json.loads(response.choices[0].message.content)

    # 🔧 Inject defaults if missing
    raw_json.setdefault("use_rag", True)
    raw_json.setdefault("use_vision", has_image)
    raw_json.setdefault("use_environment", has_location)
    raw_json.setdefault("may_need_knowledge_enrichment", False)
    raw_json.setdefault(
        "explanation",
        "Tool decision inferred based on input signals."
    )

    return ToolDecision(**raw_json)
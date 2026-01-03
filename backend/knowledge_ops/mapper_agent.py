import os
import json
from typing import Optional
from dotenv import load_dotenv
from openai import OpenAI

from backend.knowledge_ops.schema import PlantKnowledgeEntry

# --------------------------------------------------
# Load environment variables
# --------------------------------------------------
load_dotenv(override=True)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def map_proposal_to_canonical_schema(
    *,
    proposal_text: str,
    plant_name_hint: Optional[str] = None,
    created_by: str = "knowledge_mapper_agent",
) -> PlantKnowledgeEntry:
    """
    Convert free-text proposal into strict canonical schema.
    """

    system_prompt = """
You are a knowledge structuring agent.

Extract structured information and return STRICT JSON in this format:

{
  "plant_name": string,
  "symptom": string,
  "possible_causes": [string],
  "recommended_actions": [
    {
      "action": string,
      "priority": integer (1 = high, 2 = medium, 3 = low)
    }
  ],
  "confidence_score": number between 0 and 1
}

Rules:
- Do NOT invent facts
- Be conservative with confidence (<= 0.7)
- Return ONLY JSON
"""

    user_prompt = f"""
PROPOSAL:
{proposal_text}

Plant hint: {plant_name_hint or "unknown"}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    parsed = json.loads(response.choices[0].message.content)

    return PlantKnowledgeEntry(
        plant_name=parsed.get("plant_name", plant_name_hint or "unknown"),
        symptom=parsed.get("symptom", "unspecified symptom"),
        possible_causes=parsed.get("possible_causes", []),  # ✅ List[str]
        recommended_actions=parsed.get("recommended_actions", []),  # ✅ priority=int
        sources=[],  # ALWAYS empty until human-approved
        confidence={
            "score": parsed.get("confidence_score", 0.5),
            "rationale": "Estimated by mapper agent from proposal clarity"
        },
        approved=False,
        created_by=created_by,
    )
from typing import Optional, Dict, Any

# =========================
# Tool router
# =========================
from backend.agent_router.router import decide_tools

# =========================
# RAG
# =========================
from backend.rag.retriever import retrieve
from backend.rag.generator import generate_answer

# =========================
# Memory
# =========================
from backend.conversation.memory import get_memory, add_message

# =========================
# Environment
# =========================
from backend.environment.weather import fetch_weather
from backend.environment.air_quality import fetch_air_quality
from backend.environment.reasoner import summarize_environment

# =========================
# Vision
# =========================
from backend.vision.vision_embedder import extract_visual_signals


def run_orchestration(
    session_id: str,
    question: str,
    latitude: float,
    longitude: float,
    image_bytes: Optional[bytes] = None,
) -> Dict[str, Any]:
    """
    Stable orchestrator.
    No safety, no enrichment, no async agents.
    Purpose: KEEP CHATBOT WORKING.
    """

    # --------------------------------------------------
    # 1️⃣ Decide tools (ALWAYS FIRST)
    # --------------------------------------------------
    tool_plan = decide_tools(
        question=question,
        has_image=bool(image_bytes),
        has_location=True,
    )

    # --------------------------------------------------
    # 2️⃣ RAG retrieval (hard guardrail)
    # --------------------------------------------------
    chunks = retrieve(question)
    if not chunks:
        return {
            "answer": "I do not have enough information to answer this.",
            "source": "rag_guard",
            "input_mode": "text_only",
            "environment": None,
            "knowledge_proposal": None,
        }

    # --------------------------------------------------
    # 3️⃣ Conversation memory
    # --------------------------------------------------
    memory = get_memory(session_id)

    # --------------------------------------------------
    # 4️⃣ Environment signals
    # --------------------------------------------------
    weather = {}
    air = {}
    env_summary = None

    if tool_plan.use_environment:
        weather = fetch_weather(latitude, longitude)
        air = fetch_air_quality(latitude, longitude)
        env_summary = summarize_environment(weather, air)

    # --------------------------------------------------
    # 5️⃣ Vision signals
    # --------------------------------------------------
    vision_summary = None
    if tool_plan.use_vision and image_bytes:
        vision_summary = extract_visual_signals(image_bytes)

    # --------------------------------------------------
    # 6️⃣ Generate answer (ONLY LLM CALL)
    # --------------------------------------------------
    answer = generate_answer(
        question=question,
        context_chunks=chunks,
        memory=memory,
        environment_summary=env_summary,
        vision_summary=vision_summary,
    )

    # --------------------------------------------------
    # 7️⃣ Store memory
    # --------------------------------------------------
    add_message(session_id, "user", question)
    add_message(session_id, "assistant", answer)

    # --------------------------------------------------
    # 8️⃣ Final response (NO SELF-REFERENCES)
    # --------------------------------------------------
    return {
        "answer": answer,
        "source": "rag+environment+vision",
        "input_mode": "text+image" if image_bytes else "text_only",
        "environment": {
            "temperature_c": weather.get("temperature_c"),
            "humidity": weather.get("humidity"),
            "aqi": air.get("aqi"),
            "pm25": air.get("pm25"),
            "pm10": air.get("pm10"),
            "summary": env_summary,
        },
        "knowledge_proposal": None,
    }
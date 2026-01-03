from typing import Optional

# Tool planner
from backend.agent_router.router import decide_tools

# RAG
from backend.rag.retriever import retrieve
from backend.rag.generator import generate_answer

# Memory
from backend.conversation.memory import get_memory, add_message

# Environment
from backend.environment.weather import fetch_weather
from backend.environment.air_quality import fetch_air_quality
from backend.environment.reasoner import summarize_environment

# Vision
from backend.vision.vision_embedder import extract_visual_signals

# Enrichment agents (READ-ONLY)
from backend.enrichment_agent.detector import detect_knowledge_gap
from backend.enrichment_agent.proposer import propose_knowledge_enrichment
from backend.enrichment_agent.approval_store import store_proposal


def run_orchestration(
    session_id: str,
    question: str,
    latitude: float,
    longitude: float,
    image_bytes: Optional[bytes] = None,
):
    """
    Central brain of the system.
    """

    # --------------------------------------------------
    # 1️⃣ Decide tools
    # --------------------------------------------------
    tool_plan = decide_tools(
        question=question,
        has_image=bool(image_bytes),
        has_location=True,
    )

    # --------------------------------------------------
    # 2️⃣ RAG retrieval (MANDATORY)
    # --------------------------------------------------
    chunks = retrieve(question)

    if not chunks:
        return {
            "answer": "I don’t have enough knowledge to answer this request.",
            "source": "rag_guard",
            "knowledge_proposal": None,
        }

    # --------------------------------------------------
    # 3️⃣ Memory
    # --------------------------------------------------
    memory = get_memory(session_id)

    # --------------------------------------------------
    # 4️⃣ Environment
    # --------------------------------------------------
    weather, air, env_summary = {}, {}, None
    if tool_plan.use_environment:
        weather = fetch_weather(latitude, longitude)
        air = fetch_air_quality(latitude, longitude)
        env_summary = summarize_environment(weather, air)

    # --------------------------------------------------
    # 5️⃣ Vision
    # --------------------------------------------------
    vision_summary = None
    if tool_plan.use_vision and image_bytes:
        vision_summary = extract_visual_signals(image_bytes)

    # --------------------------------------------------
    # 6️⃣ Answer generation (ONLY OpenAI usage)
    # --------------------------------------------------
    answer = generate_answer(
        question=question,
        context_chunks=chunks,
        memory=memory,
        environment_summary=env_summary,
        vision_summary=vision_summary,
    )

    # --------------------------------------------------
    # 7️⃣ Knowledge gap detection
    # --------------------------------------------------
    gap_detected = detect_knowledge_gap(
        user_question=question,
        rag_chunks=chunks,
        llm_answer=answer,
        environment_summary=env_summary,
        vision_summary=vision_summary,
    )

    proposal = None
    proposal_id = None

    # --------------------------------------------------
    # 8️⃣ Knowledge proposal (NON-BLOCKING)
    # --------------------------------------------------
    if gap_detected:
        proposal = propose_knowledge_enrichment(
            user_question=question,
            rag_chunks=chunks,
            llm_answer=answer,
            environment_summary=env_summary,
            vision_summary=vision_summary,
        )
        if proposal:
            proposal_id = store_proposal(proposal)

    # --------------------------------------------------
    # 9️⃣ Memory persistence
    # --------------------------------------------------
    add_message(session_id, "user", question)
    add_message(session_id, "assistant", answer)

    # --------------------------------------------------
    # 🔟 Final response
    # --------------------------------------------------
    return {
        "answer": answer,
        "source": "rag+llm+memory+environment+vision",
        "environment": {
            "temperature_c": weather.get("temperature_c"),
            "humidity": weather.get("humidity"),
            "aqi": air.get("aqi"),
            "pm25": air.get("pm25"),
            "pm10": air.get("pm10"),
            "summary": env_summary,
        },
        "knowledge_proposal": proposal.dict() if proposal else None,
        "knowledge_proposal_id": proposal_id,
    }
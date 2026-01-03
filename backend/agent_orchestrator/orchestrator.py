from typing import Optional

# Tool routing
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

# Enrichment (read-only)
from backend.enrichment_agent.detector import detect_knowledge_gap
from backend.enrichment_agent.proposer import propose_knowledge_enrichment
from backend.enrichment_agent.approval_store import store_proposal

# Safety
from backend.safety.disclaimer_agent import inject_disclaimer


def run_orchestration(
    session_id: str,
    question: str,
    latitude: Optional[float],
    longitude: Optional[float],
    image_bytes: Optional[bytes],
):
    """
    Central orchestration brain.
    This function owns ALL execution flow.
    """

    # --------------------------------------------------
    # 1️⃣ Decide which tools to run
    # --------------------------------------------------
    tool_plan = decide_tools(
        question=question,
        has_image=bool(image_bytes),
        has_location=bool(latitude and longitude),
    )

    # --------------------------------------------------
    # 2️⃣ RAG retrieval (authoritative)
    # --------------------------------------------------
    chunks = retrieve(question)

    if not chunks:
        return {
            "answer": "I do not have enough information.",
            "source": "rag_guard",
            "input_mode": "text_only",
            "environment": None,
            "knowledge_proposal": None,
            "knowledge_proposal_id": None,
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

    if tool_plan.use_environment and latitude and longitude:
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
    # 6️⃣ Generate grounded answer (ONLY LLM CALL)
    # --------------------------------------------------
    answer = generate_answer(
        question=question,
        context_chunks=chunks,
        memory=memory,
        environment_summary=env_summary,
        vision_summary=vision_summary,
    )

    # --------------------------------------------------
    # 7️⃣ Knowledge gap detection + proposal
    # --------------------------------------------------
    proposal = None
    proposal_id = None

    gap_detected = detect_knowledge_gap(
        user_question=question,
        rag_chunks=chunks,
        llm_answer=answer,
        environment_summary=env_summary,
        vision_summary=vision_summary,
    )

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
    # 8️⃣ Determine input mode (IMPORTANT FIX)
    # --------------------------------------------------
    if question and image_bytes:
        input_mode = "text+image"
    elif image_bytes:
        input_mode = "image_only"
    else:
        input_mode = "text_only"

    # --------------------------------------------------
    # 9️⃣ Safety disclaimer injection
    # --------------------------------------------------
    final_answer = inject_disclaimer(
        answer=answer,
        input_mode=input_mode,
        used_vision=bool(vision_summary),
        used_environment=bool(env_summary),
    )

    # --------------------------------------------------
    # 🔟 Store memory
    # --------------------------------------------------
    add_message(session_id, "user", question)
    add_message(session_id, "assistant", final_answer)

    # --------------------------------------------------
    # 🧾 Final response
    # --------------------------------------------------
    return {
        "answer": final_answer,
        "source": "rag+llm+orchestrated",
        "input_mode": input_mode,
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
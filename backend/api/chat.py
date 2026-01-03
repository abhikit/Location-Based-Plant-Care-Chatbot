from fastapi import APIRouter, UploadFile, File, Form, HTTPException, BackgroundTasks
from typing import Optional

# =========================
# Orchestrator (SINGLE BRAIN)
# =========================
from backend.agent_orchestrator.orchestrator import run_orchestration

# =========================
# Phase-3C: Async Enrichment
# =========================
from backend.enrichment_agent.background import run_async_enrichment

router = APIRouter()


@router.post("/chat")
def chat(
    background_tasks: BackgroundTasks,
    session_id: str = Form(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    question: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
):
    """
    Main chat endpoint (Phase-3B + Phase-3C compliant)

    Supports:
    - text only
    - image only
    - text + image

    Guarantees:
    - No-RAG-No-Answer
    - Grounded answers only
    - Environment-aware
    - Vision-aware
    - Agentic enrichment (ASYNC, non-blocking)
    """

    # --------------------------------------------------
    # 0️⃣ Input validation
    # --------------------------------------------------
    if not question and not image:
        raise HTTPException(
            status_code=400,
            detail="Please provide either a question, an image, or both.",
        )

    # --------------------------------------------------
    # 1️⃣ Effective user intent
    # --------------------------------------------------
    effective_question = question
    if not effective_question and image:
        effective_question = (
            "The user has uploaded a plant image. "
            "Describe visible symptoms and provide care guidance "
            "ONLY if supported by plant knowledge."
        )

    # --------------------------------------------------
    # 2️⃣ Read image bytes ONCE (important)
    # --------------------------------------------------
    image_bytes = image.file.read() if image else None

    # --------------------------------------------------
    # 3️⃣ ORCHESTRATOR (SYNC, USER-CRITICAL PATH)
    # --------------------------------------------------
    orchestration_result = run_orchestration(
        session_id=session_id,
        question=effective_question,
        latitude=latitude,
        longitude=longitude,
        image_bytes=image_bytes,
    )

    # --------------------------------------------------
    # 4️⃣ ASYNC ENRICHMENT (NON-BLOCKING)
    # --------------------------------------------------
    background_tasks.add_task(
        run_async_enrichment,
        user_question=effective_question,
        rag_chunks=orchestration_result.get("rag_chunks", []),
        llm_answer=orchestration_result.get("answer"),
        environment_summary=orchestration_result.get("environment", {}).get("summary"),
        vision_summary=orchestration_result.get("vision_summary"),
    )

    # --------------------------------------------------
    # 5️⃣ Return user response immediately
    # --------------------------------------------------
    return orchestration_result
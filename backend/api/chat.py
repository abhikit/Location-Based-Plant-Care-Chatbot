from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional

from backend.rag.retriever import retrieve
from backend.rag.generator import generate_answer
from backend.conversation.memory import get_memory, add_message

from backend.environment.weather import fetch_weather
from backend.environment.air_quality import fetch_air_quality
from backend.environment.reasoner import summarize_environment

from backend.vision.vision_embedder import extract_visual_signals

router = APIRouter()


@router.post("/chat")
def chat(
    session_id: str = Form(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    question: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None)
):
    # ❌ Case: Neither text nor image provided
    if not question and not image:
        raise HTTPException(
            status_code=400,
            detail="Please provide either a question, an image, or both."
        )

    # 🧠 If no question but image exists, create implicit intent
    effective_question = question
    if not effective_question and image:
        effective_question = (
            "The user has uploaded a plant image. "
            "Describe visible symptoms and provide care guidance "
            "only if supported by plant knowledge."
        )

    # 1️⃣ RAG retrieval (ALWAYS based on text intent)
    chunks = retrieve(effective_question)

    # 🔒 RAG guardrail
    if not chunks:
        return {
            "answer": "I don’t have enough knowledge to answer this request.",
            "source": "rag_guard"
        }

    # 2️⃣ Memory
    memory = get_memory(session_id)

    # 3️⃣ Environment
    weather = fetch_weather(latitude, longitude)
    air = fetch_air_quality(latitude, longitude)
    env_summary = summarize_environment(weather, air)

    # 4️⃣ Vision (optional)
    vision_summary = None
    if image:
        image_bytes = image.file.read()
        vision_summary = extract_visual_signals(image_bytes)

    # 5️⃣ Generate grounded answer
    answer = generate_answer(
        effective_question,
        chunks,
        memory,
        environment_summary=env_summary,
        vision_summary=vision_summary
    )

    # 6️⃣ Store memory (only real user text, not synthetic)
    if question:
        add_message(session_id, "user", question)
    add_message(session_id, "assistant", answer)

    return {
        "answer": answer,
        "source": "rag+llm+memory+environment+vision",
        "input_mode": (
            "text+image" if question and image
            else "image_only" if image
            else "text_only"
        ),
        "environment": {
            "temperature": weather.get("temperature_c"),
            "humidity": weather.get("humidity"),
            "aqi": air.get("aqi"),
            "pm25": air.get("pm25"),
            "pm10": air.get("pm10"),
            "summary": env_summary
        }
    }
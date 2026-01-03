from backend.knowledge_ops.schema import PlantKnowledgeEntry


def promote_to_knowledge_base(entry: PlantKnowledgeEntry):
    """
    FINAL GATE before entering RAG KB.

    In Phase-6 this will:
    - Embed
    - Chunk
    - Store in vector DB
    """

    # Phase-5C: Stub only (SAFE)
    print(f"[PROMOTED] {entry.plant_name} — {entry.symptom}")
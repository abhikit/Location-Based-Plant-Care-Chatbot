from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
VECTOR_STORE_PATH = PROJECT_ROOT / "vector_store"

COLLECTION_NAME = "plant_knowledge"
import json
import uuid
from pathlib import Path
from backend.human_review.models import HumanReviewDecision

STORE_PATH = Path("human_reviews")
STORE_PATH.mkdir(exist_ok=True)


def store_human_review(decision: HumanReviewDecision) -> str:
    review_id = str(uuid.uuid4())
    file_path = STORE_PATH / f"{review_id}.json"

    with open(file_path, "w") as f:
        json.dump(decision.dict(), f, indent=2, default=str)

    return review_id


def list_reviews():
    return [p.name for p in STORE_PATH.glob("*.json")]
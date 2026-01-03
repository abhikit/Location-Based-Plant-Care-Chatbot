from fastapi import APIRouter
from backend.human_review.models import HumanReviewDecision
from backend.human_review.store import store_human_review, list_reviews

router = APIRouter(prefix="/human-review", tags=["Human Review"])


@router.post("/submit")
def submit_review(decision: HumanReviewDecision):
    review_id = store_human_review(decision)
    return {
        "status": "saved",
        "review_id": review_id
    }


@router.get("/list")
def get_all_reviews():
    return {
        "reviews": list_reviews()
    }
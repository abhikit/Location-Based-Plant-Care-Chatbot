from enum import Enum


class KnowledgeState(str, Enum):
    DETECTED = "detected"
    PROPOSED = "proposed"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    ARCHIVED = "archived"
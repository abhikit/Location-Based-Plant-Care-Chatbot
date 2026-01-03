from pydantic import BaseModel


class ToolDecision(BaseModel):
    use_rag: bool = True
    use_environment: bool = False
    use_vision: bool = False
    run_gap_detection: bool = False
    run_proposal_agent: bool = False
    explanation: str
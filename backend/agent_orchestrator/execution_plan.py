from dataclasses import dataclass

@dataclass
class ExecutionPlan:
    use_rag: bool = True
    use_environment: bool = False
    use_vision: bool = False
    run_enrichment_agents: bool = False
from pathlib import Path
import json
from collections import Counter

LOG_DIR = Path("compliance_logs")


def compliance_metrics():
    events = []
    for f in LOG_DIR.glob("*.json"):
        with open(f) as fh:
            events.append(json.load(fh))

    return {
        "total_requests": len(events),
        "risk_distribution": Counter(e["risk_level"] for e in events),
        "disclaimer_rate": sum(e["disclaimer_injected"] for e in events),
        "knowledge_proposals": sum(1 for e in events if e["knowledge_proposal_id"]),
    }
from collections import defaultdict
from typing import List, Dict

# Simple in-memory store
# { session_id: [ {"role": "user"/"assistant", "content": "..."} ] }
_MEMORY_STORE: Dict[str, List[Dict[str, str]]] = defaultdict(list)


def get_memory(session_id: str, limit: int = 6):
    """
    Return last N messages for a session.
    Memory is conversational context ONLY.
    """
    return _MEMORY_STORE[session_id][-limit:]


def add_message(session_id: str, role: str, content: str):
    _MEMORY_STORE[session_id].append({
        "role": role,
        "content": content
    })
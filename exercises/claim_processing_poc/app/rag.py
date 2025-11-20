import json
from typing import List, Dict


def load_policies(path: str) -> List[Dict]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _tokenize(text: str) -> set:
    return set([t.strip(".,;:!?()[]{}\"'").lower() for t in text.split() if t.strip()])


def retrieve_relevant_policies(query_text: str, policies: List[Dict], k: int = 3) -> List[Dict]:
    """
    Naive keyword-overlap retriever. Replace with embeddings/vector DB for production.
    """
    q_tokens = _tokenize(query_text)
    scored = []
    for p in policies:
        text = p.get("text", "")
        p_tokens = _tokenize(text)
        overlap = len(q_tokens & p_tokens)
        scored.append((overlap, p))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [p for _, p in scored[:k]]


def format_policy_context(policies: List[Dict]) -> str:
    parts = []
    for p in policies:
        title = p.get("title", "Policy")
        text = p.get("text", "")
        parts.append(f"{title}:\n{text}")
    return "\n\n".join(parts)



"""Multi-source response synthesis and quality/confidence assessment for RAG."""

from typing import List, Dict
from sentence_transformers import CrossEncoder

# Example: use a cross-encoder for re-ranking (must have model downloaded)
CROSS_ENCODER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

cross_encoder = None

def get_cross_encoder():
    global cross_encoder
    if cross_encoder is None:
        cross_encoder = CrossEncoder(CROSS_ENCODER_MODEL)
    return cross_encoder


def synthesize_response(sources: List[Dict], query: str) -> Dict:
    """Aggregate multiple sources, resolve conflicts, and score confidence."""
    # 1. Re-rank sources using cross-encoder
    ce = get_cross_encoder()
    pairs = [(query, s["snippet"]) for s in sources]
    scores = ce.predict(pairs)
    ranked = sorted(zip(sources, scores), key=lambda x: x[1], reverse=True)
    # 2. Synthesize answer from top sources
    answer = " ".join([r[0]["snippet"] for r in ranked[:3]])
    # 3. Confidence score (mean of top scores)
    confidence = float(sum(scores[:3]) / max(1, len(scores[:3])))
    # 4. Quality assessment: simple heuristic (can be replaced with LLM)
    quality = "high" if confidence > 0.7 else "medium" if confidence > 0.4 else "low"
    return {
        "answer": answer,
        "confidence": confidence,
        "quality": quality,
        "sources": [r[0] for r in ranked[:3]],
    }


def resolve_conflicts(sources: List[Dict]) -> List[Dict]:
    """Basic conflict resolution: deduplicate by snippet/content."""
    seen = set()
    unique = []
    for s in sources:
        content = s.get("snippet", "")
        if content not in seen:
            seen.add(content)
            unique.append(s)
    return unique

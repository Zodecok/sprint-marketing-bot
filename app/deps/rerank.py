from __future__ import annotations
from functools import lru_cache
from typing import List, Tuple

try:
    from sentence_transformers import CrossEncoder
    CE_AVAILABLE = True
except Exception:
    CrossEncoder = None
    CE_AVAILABLE = False

@lru_cache(maxsize=1)
def get_reranker(model_name: str):
    if not CE_AVAILABLE:
        raise RuntimeError("CrossEncoder not available; install torch + sentence-transformers or disable rerank.")
    return CrossEncoder(model_name)

def rerank(query: str, passages: List[Tuple[float, dict]], model_name: str, top_k: int) -> List[Tuple[float, dict]]:
    pairs = [(query, p[1]["chunk"]) for p in passages]
    scores = get_reranker(model_name).predict(pairs)  # higher = better
    out = [(float(scores[i]), passages[i][1]) for i in range(len(passages))]
    out.sort(key=lambda x: x[0], reverse=True)
    return out[:top_k]

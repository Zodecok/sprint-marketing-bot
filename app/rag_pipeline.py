import numpy as np
from typing import List, Tuple
from app.settings import settings
from app.deps.embeddings import embed_texts
from app.deps.vectorstore import load_index
from app.deps.rerank import rerank as ce_rerank, CE_AVAILABLE


def _cosine_norm(vecs: np.ndarray) -> np.ndarray:
    return vecs / (np.linalg.norm(vecs, axis=1, keepdims=True) + 1e-12)

def retrieve(query: str, k: int) -> List[Tuple[float, dict]]:
    index, metas = load_index()
    qvec = np.array(embed_texts([query]), dtype="float32")
    qvec = _cosine_norm(qvec)  # cosine via inner product

    n_candidates = int(settings.retrieval_candidates)
    # D is similarity scores, I is indices into metas
    D, I = index.search(qvec, k)

    # similarity score with metadata
    prelim: List[Tuple[float, dict]] = [(float(s), metas[i]) for s, i in zip(D[0].tolist(), I[0].tolist())]

    use_rerank = str(settings.enable_rerank).lower() == "true" and CE_AVAILABLE
    if use_rerank:
        reranked = ce_rerank(query, prelim, settings.reranker_model, max(k, 10))
        results = [(s, m) for (s, m) in reranked]                # CE scores
    else:
        prelim.sort(key=lambda x: x[0], reverse=True)            # vector scores
        results = prelim

    # Similarity floor
    min_sim = float(settings.min_sim)
    results = [r for r in results if r[0] >= min_sim]

    return results[:k]

def build_prompt(query: str, contexts: List[dict]) -> str:
    # Deterministic prompt that forces source usage + inline citations [#]

    # contexts is a list of dicts with keys: chunk, doc_path, chunk_id
    blocks = []
    for i, c in enumerate(contexts):
        blocks.append(
            f"[{i+1}] {c['chunk']}\n"
            f"(SOURCE: {c['doc_path']} | CHUNK_ID: {c['chunk_id']})"
        )
    context_blob = "\n\n".join(blocks)
    return (
        "You are a Sprint Marketing assistant. Answer ONLY with facts from the provided sources. "
        "If the answer is not in the sources, say you don’t have that information. "
        "Cite sources inline like [1], [2]. At the end, add a 'Sources' line listing the doc_path and chunk_ids you used.\n\n"
        f"User question: {query}\n\n"
        f"SOURCES:\n{context_blob}\n\n"
        "Answer:\n"
    )

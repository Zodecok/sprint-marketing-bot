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
    """
    Build a customer-facing prompt for the LLM (Large Language Model).
    - Uses only the chunk text (no paths/IDs) to avoid leaking internal metadata.
    - Instructs the model to write a concise, friendly, benefit-led answer.
    - If info is missing, respond honestly and suggest a next step.
    - No citations or brackets like [1], [2] in the output.
    """
    # contexts is a list of dicts with keys: chunk, doc_path, chunk_id
    # We intentionally do NOT include doc_path/chunk_id in the context we show the LLM.
    blocks = [c["chunk"] for c in contexts]
    context_blob = "\n\n---\n\n".join(blocks) if blocks else "[No relevant knowledge]"

    return (
        "You are Sprint Marketing’s assistant for prospective customers.\n"
        "Write a concise, friendly answer using only the Knowledge below.\n"
        "DO NOT show citations, file names, chunk IDs, or internal notes.\n"
        "If the answer is not in the Knowledge, say you don't have that information and suggest a next step.\n"
        "\n"
        "Style rules:\n"
        "- Lead with the customer benefit.\n"
        "- Prefer plain language and short paragraphs or tight bullet points.\n"
        "- Keep it under ~120 words when possible.\n"
        "- End with a simple call to action (e.g., how to contact or book a call).\n"
        "\n"
        f"Customer question:\n{query}\n\n"
        f"Knowledge:\n{context_blob}\n\n"
        "Now draft the reply:\n"
    )

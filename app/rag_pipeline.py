import numpy as np
from typing import List, Tuple
from app.settings import settings
from app.deps.embeddings import embed_texts
from app.deps.vectorstore import load_index

def retrieve(query: str, k: int) -> List[Tuple[float, dict]]:
    index, metas = load_index()
    qvec = np.array(embed_texts([query]), dtype="float32")
    qvec = qvec / (np.linalg.norm(qvec, axis=1, keepdims=True) + 1e-12)  # cosine via inner product
    # D is similarity scores, I is indices into metas
    D, I = index.search(qvec, k)
    out: List[Tuple[float, dict]] = []

    # zips toegether scores and metadata then returns it in a list of tuples
    # Each tuple contains (score, metadata)
    for score, idx in zip(D[0].tolist(), I[0].tolist()):
        out.append((float(score), metas[idx]))
    return out

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

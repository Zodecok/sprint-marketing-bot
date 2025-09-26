from pathlib import Path
import numpy as np, hashlib, faiss
from tqdm import tqdm
from app.settings import settings
from app.deps.chunking import read_text_from_path, chunk_text
from app.deps.embeddings import embed_texts
from app.deps.vectorstore import save_index
import hashlib, json
from datetime import datetime, timezone

DOCS_DIR = Path("docs")
MANIFEST_PATH = Path("data/index_manifest.json")

def _hash_index(metas: list[dict]) -> str:
    """Stable version hash from chunk_ids (and counts)."""
    h = hashlib.sha256()
    h.update(str(len(metas)).encode())
    for m in metas:
        h.update(m["chunk_id"].encode())
    return h.hexdigest()[:16]  # short version tag

def _write_manifest(metas: list[dict], files_count: int, chunks_count: int):
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    manifest = {
        "index_version": _hash_index(metas),
        "built_at": datetime.now(timezone.utc).isoformat(),
        "files_count": files_count,
        "chunks_count": chunks_count,
    }
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

def _chunk_id(doc_path: str, idx: int, chunk: str) -> str:
    return hashlib.sha1((doc_path + str(idx) + chunk[:64]).encode("utf-8")).hexdigest()[:12]

# TODO: modify to use resource files that are laid out already separated by content type
# this is later to increase the effectiveness of the reranker and vectorisation
def run_ingest() -> tuple[int, int]:
    files = [p for p in DOCS_DIR.glob("**/*") if p.is_file()]
    metas, chunks = [], []
    for f in tqdm(files, desc="Docs"):
        text = read_text_from_path(f)
        for i, c in enumerate(chunk_text(text, settings.chunk_size, settings.chunk_overlap)):
            metas.append({"doc_path": str(f), "chunk_id": _chunk_id(str(f), i, c), "chunk": c})
            chunks.append(c)

    if not chunks:
        raise RuntimeError("No chunks found. Put files in /docs.")

    vecs = np.array(embed_texts(chunks), dtype="float32")
    vecs = vecs / (np.linalg.norm(vecs, axis=1, keepdims=True) + 1e-12)

    index = faiss.IndexFlatIP(vecs.shape[1])
    index.add(vecs)

    Path("data").mkdir(exist_ok=True)
    save_index(index, metas)

    # writing ingest manifest
    _write_manifest(metas, len(files), len(chunks))
    return len(files), len(chunks)

if __name__ == "__main__":
    files, chunks = run_ingest()
    print(f"Ingested {files} files into {chunks} chunks")

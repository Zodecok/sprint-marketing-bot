from pathlib import Path
import numpy as np, hashlib, faiss
from tqdm import tqdm
from app.settings import settings
from app.deps.chunking import read_text_from_path, chunk_text
from app.deps.embeddings import embed_texts
from app.deps.vectorstore import save_index

DOCS_DIR = Path("docs")

def _chunk_id(doc_path: str, idx: int, chunk: str) -> str:
    return hashlib.sha1((doc_path + str(idx) + chunk[:64]).encode("utf-8")).hexdigest()[:12]

def run_ingest() -> tuple[int, int]:
    files = [p for p in DOCS_DIR.glob("**/*") if p.is_file()]
    metas, chunks = [], []
    for f in tqdm(files, desc="Docs"):
        text = read_text_from_path(f)
        print("This is the chunks", settings.chunk_size, settings.chunk_overlap)
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
    return len(files), len(chunks)

if __name__ == "__main__":
    files, chunks = run_ingest()
    print(f"Ingested {files} files into {chunks} chunks")

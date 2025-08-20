import json, os, faiss
import numpy as np
from pathlib import Path
from typing import List, Tuple

INDEX_PATH = "data/index.faiss"
META_PATH  = "data/meta.jsonl"

def save_index(index: faiss.IndexFlatIP, metas: List[dict]):
    faiss.write_index(index, INDEX_PATH)
    with open(META_PATH, "w", encoding="utf-8") as f:
        for m in metas:
            f.write(json.dumps(m, ensure_ascii=False) + "\n")

def load_index() -> Tuple[faiss.IndexFlatIP, list[dict]]:
    if not (os.path.exists(INDEX_PATH) and os.path.exists(META_PATH)):
        raise FileNotFoundError("No index found. Run ingest first.")
    index = faiss.read_index(INDEX_PATH)
    metas = [json.loads(line) for line in open(META_PATH, "r", encoding="utf-8")]
    return index, metas

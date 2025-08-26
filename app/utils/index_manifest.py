from __future__ import annotations
from pathlib import Path
import json

_MANIFEST = Path("data/index_manifest.json")

def read_index_manifest() -> dict:
    if _MANIFEST.exists():
        try:
            return json.loads(_MANIFEST.read_text(encoding="utf-8"))
        except Exception:
            pass
    # sensible defaults when manifest missing
    return {"index_version": "unknown", "built_at": None, "files_count": 0, "chunks_count": 0}

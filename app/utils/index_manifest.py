from __future__ import annotations
import json
from app.utils.paths import index_manifest_path, index_dir


def read_index_manifest() -> dict:
    manifest_path = index_manifest_path()
    if manifest_path.exists():
        try:
            return json.loads(manifest_path.read_text(encoding="utf-8"))
        except Exception:
            pass
    # Fall back to legacy manifest if present
    legacy_path = index_dir().parent / "index_manifest.json"
    if legacy_path.exists():
        try:
            return json.loads(legacy_path.read_text(encoding="utf-8"))
        except Exception:
            pass
    # sensible defaults when manifest missing
    index_dir().mkdir(parents=True, exist_ok=True)
    return {"index_version": "unknown", "built_at": None, "files_count": 0, "chunks_count": 0}

from __future__ import annotations
from pathlib import Path
from datetime import datetime, timezone
import json
import re

LOG_DIR = Path("data/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

def _redact(text: str) -> str:
    # Very light PII redaction (emails/phones). Extend as needed.
    text = re.sub(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", "[redacted-email]", text)
    text = re.sub(r"\b(\+?\d[\d\s\-().]{7,}\d)\b", "[redacted-phone]", text)
    return text

def log_chat(query: str, answer: str, hits):
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "query": _redact(query)[:1000],
        "answer_preview": _redact(answer)[:400],
        "hits": [
            {"score": float(s), "doc_path": m["doc_path"], "chunk_id": m["chunk_id"]}
            for (s, m) in hits
        ],
    }
    dayfile = LOG_DIR / (datetime.now(timezone.utc).strftime("%Y%m%d") + ".jsonl")
    with dayfile.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

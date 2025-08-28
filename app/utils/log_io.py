import os, json, time, threading
from typing import Any, Dict, Iterable

_LOCKS = {}
def _lock_for(path: str) -> threading.Lock:
    if path not in _LOCKS:
        _LOCKS[path] = threading.Lock()
    return _LOCKS[path]

def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def jsonl_append(path: str, record: Dict[str, Any]) -> None:
    lock = _lock_for(path)
    ensure_dir(os.path.dirname(path))
    with lock:
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

def jsonl_tail(path: str, n: int) -> Iterable[Dict[str, Any]]:
    if not os.path.exists(path):
        return []
    # Fast-ish tail without loading whole file for small logs
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()[-n:]
    out = []
    for line in lines:
        line = line.strip()
        if not line: 
            continue
        try:
            out.append(json.loads(line))
        except Exception:
            continue
    return out

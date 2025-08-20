from typing import Iterable
from pathlib import Path
from pypdf import PdfReader
import docx
import re

def _normalize_ws(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()

def read_text_from_path(path: Path) -> str:
    if path.suffix.lower() == ".pdf":
        reader = PdfReader(str(path))
        return _normalize_ws(" ".join(page.extract_text() or "" for page in reader.pages))
    if path.suffix.lower() == ".docx":
        d = docx.Document(str(path))
        return _normalize_ws(" ".join(p.text for p in d.paragraphs))
    if path.suffix.lower() in {".md", ".txt"}:
        return _normalize_ws(path.read_text(encoding="utf-8", errors="ignore"))
    return ""

def chunk_text(text: str, chunk_size: int = 800, overlap: int = 150) -> Iterable[str]:
    tokens = text.split()
    chunks = []
    i = 0
    while i < len(tokens):
        chunk = " ".join(tokens[i:i+chunk_size])
        chunks.append(chunk)
        i += (chunk_size - overlap)
    return chunks

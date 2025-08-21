from pydantic import BaseModel
from typing import List

class ChatRequest(BaseModel):
    query: str

class Source(BaseModel):
    doc_path: str
    chunk_id: str
    score: float
    preview: str

class ChatResponse(BaseModel):
    answer: str
    sources: List[Source]

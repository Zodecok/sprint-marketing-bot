from pydantic import BaseModel
from typing import List

class ChatRequest(BaseModel):
    query: str


class ChatResponse(BaseModel):
    answer: str
    has_sources: bool = True
    sources_count = 0
    request_id: str

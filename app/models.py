from pydantic import BaseModel

class ChatRequest(BaseModel):
    query: str


class ChatResponse(BaseModel):
    answer: str
    has_sources: bool = True
    sources_count: int = 0
    request_id: str

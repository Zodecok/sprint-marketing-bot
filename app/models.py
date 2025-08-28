from pydantic import BaseModel, Field
from typing import List, Optional

class ChatRequest(BaseModel):
    query: str


class ChatResponse(BaseModel):
    answer: str
    has_sources: bool = True
    source_count: int = 0
    request_id: str


# Request model for UI event ingestion
class UIEventIn(BaseModel):
    name: str = Field(..., description="Event name, e.g., widget_open, chat_send")
    payload: Optional[dict] = Field(default=None, description="Arbitrary event data")
    ts: Optional[int] = Field(default=None, description="Client timestamp (ms since epoch)")


# Response models for conversations list
class ConversationSummary(BaseModel):
    ts: int = Field(..., description="Server timestamp (ms since epoch)")
    user: str = Field("", description="First user message snippet")
    assistant: str = Field("", description="Assistant reply snippet")


class ConversationList(BaseModel):
    items: List[ConversationSummary]

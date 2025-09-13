from __future__ import annotations
from typing import Optional
from pydantic import BaseModel


class ChatMessageRequest(BaseModel):
    conversation_id: Optional[str] = None
    content: str


class ChatMessageResponse(BaseModel):
    conversation_id: str
    message_id: str
    stream_url: str


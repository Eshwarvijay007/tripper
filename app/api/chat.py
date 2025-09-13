from __future__ import annotations
import uuid
from typing import Iterator
from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse
from ..schemas.chat import ChatMessageRequest, ChatMessageResponse
from ..services.store import CONVERSATIONS, MESSAGES


router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("/messages", response_model=ChatMessageResponse)
def post_message(req: ChatMessageRequest):
    conv_id = req.conversation_id or str(uuid.uuid4())
    if conv_id not in CONVERSATIONS:
        CONVERSATIONS[conv_id] = {"id": conv_id, "messages": []}
    msg_id = str(uuid.uuid4())
    MESSAGES[msg_id] = {"id": msg_id, "conv_id": conv_id, "role": "user", "content": req.content}
    CONVERSATIONS[conv_id]["messages"].append(msg_id)
    return ChatMessageResponse(
        conversation_id=conv_id,
        message_id=msg_id,
        stream_url=f"/api/chat/stream/{conv_id}"
    )


def _stream_stub(conv_id: str) -> Iterator[bytes]:
    # Simple JSONL stream to simulate tokens
    payloads = [
        {"event": "start", "conversation_id": conv_id},
        {"event": "token", "text": "Planning your trip... "},
        {"event": "token", "text": "Finding flights... "},
        {"event": "token", "text": "Finding hotels... "},
        {"event": "done"},
    ]
    for p in payloads:
        line = (str(p) + "\n").encode("utf-8")
        yield line


@router.get("/stream/{conversation_id}")
def stream(conversation_id: str):
    return StreamingResponse(_stream_stub(conversation_id), media_type="application/x-ndjson")


@router.get("/messages")
def list_messages(conversation_id: str = Query(...)) -> dict:
    conv = CONVERSATIONS.get(conversation_id)
    if not conv:
        return {"messages": []}
    msgs = [MESSAGES[mid] for mid in conv.get("messages", [])]
    # Normalize response shape
    out = [{"id": m["id"], "role": m["role"], "content": m["content"]} for m in msgs]
    return {"messages": out}


@router.post("/stop")
def stop_stream(conversation_id: str):
    conv = CONVERSATIONS.get(conversation_id)
    if conv is None:
        return {"stopped": False}
    conv["stopped"] = True
    return {"stopped": True}

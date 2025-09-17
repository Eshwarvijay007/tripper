from __future__ import annotations
import uuid
from typing import Iterator
from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage
from ..schemas.chat import ChatMessageRequest, ChatMessageResponse
from ..services.conversation_repository import (
    append_message,
    ensure_conversation,
    get_last_user_message,
    get_messages,
    set_conversation_stopped,
)
from ..ai.chat_graph import graph


router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("/messages", response_model=ChatMessageResponse)
def post_message(req: ChatMessageRequest):
    conv_id = req.conversation_id or str(uuid.uuid4())
    ensure_conversation(conv_id)
    msg_id = str(uuid.uuid4())
    append_message(conv_id, msg_id, "user", req.content)
    return ChatMessageResponse(
        conversation_id=conv_id,
        message_id=msg_id,
        stream_url=f"/api/chat/stream/{conv_id}"
    )


def _stream_assistant(conv_id: str) -> Iterator[bytes]:
    # Fetch the most recent user message content
    user_msg = get_last_user_message(conv_id)
    if not user_msg:
        yield str({"event": "error", "message": "No conversation or message found"}).encode() + b"\n"
        return

    # Stream: start → single assistant reply → done
    yield (str({"event": "start", "conversation_id": conv_id}) + "\n").encode("utf-8")
    try:
        config = {"configurable": {"thread_id": conv_id}}
        out = graph.invoke({"messages": [HumanMessage(content=user_msg["content"])]}, config=config)
        # Emit one message event with assistant content
        msgs = out.get("messages") or []
        text = ""
        for m in msgs:
            if getattr(m, "type", None) == "ai":
                text = getattr(m, "content", "") or ""
        yield (str({"event": "message", "role": "assistant", "content": text}) + "\n").encode("utf-8")
        if text:
            assistant_id = str(uuid.uuid4())
            append_message(conv_id, assistant_id, "assistant", text)
        yield (str({"event": "done"}) + "\n").encode("utf-8")
    except Exception as e:
        yield (str({"event": "error", "message": str(e)}) + "\n").encode("utf-8")


@router.get("/stream/{conversation_id}")
def stream(conversation_id: str):
    return StreamingResponse(_stream_assistant(conversation_id), media_type="application/x-ndjson")


@router.get("/messages")
def list_conversation_messages(conversation_id: str = Query(...)) -> dict:
    msgs = get_messages(conversation_id)
    return {"messages": msgs}


@router.post("/stop")
def stop_stream(conversation_id: str):
    set_conversation_stopped(conversation_id, True)
    return {"stopped": True}

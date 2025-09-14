from __future__ import annotations
import uuid
from typing import Iterator
from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage
from ..schemas.chat import ChatMessageRequest, ChatMessageResponse
from ..services.store import CONVERSATIONS, MESSAGES
from ..ai.chat_graph import graph


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


def _stream_assistant(conv_id: str) -> Iterator[bytes]:
    # Fetch the most recent user message content
    conv = CONVERSATIONS.get(conv_id)
    if not conv or not conv.get("messages"):
        yield str({"event": "error", "message": "No conversation or message found"}).encode() + b"\n"
        return
    last_msg_id = conv["messages"][-1]
    user_msg = MESSAGES.get(last_msg_id)
    if not user_msg or user_msg.get("role") != "user":
        yield str({"event": "error", "message": "Last message is not a user message"}).encode() + b"\n"
        return

    # Stream: start → single assistant reply → done
    import json
    yield (json.dumps({"event": "start", "conversation_id": conv_id}) + "\n").encode("utf-8")
    try:
        config = {"configurable": {"thread_id": conv_id}}
        out = graph.invoke({"messages": [HumanMessage(content=user_msg["content"])]}, config=config)
        # Emit one message event with assistant content
        msgs = out.get("messages") or []
        text = ""
        for m in msgs:
            if getattr(m, "type", None) == "ai":
                text = getattr(m, "content", "") or ""
        yield (json.dumps({"event": "message", "role": "assistant", "content": text}) + "\n").encode("utf-8")
        yield (json.dumps({"event": "done"}) + "\n").encode("utf-8")
    except RuntimeError as e:
        yield (json.dumps({"event": "error", "message": str(e)}) + "\n").encode("utf-8")


@router.get("/stream/{conversation_id}")
def stream(conversation_id: str):
    return StreamingResponse(_stream_assistant(conversation_id), media_type="application/x-ndjson")


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

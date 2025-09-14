from __future__ import annotations
import uuid
from typing import Iterator
from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage, AIMessage
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


def _to_lc_messages(conv: dict) -> list:
    lc_msgs = []
    for mid in conv.get("messages", []):
        m = MESSAGES.get(mid)
        if not m:
            continue
        role = m.get("role")
        content = m.get("content") or ""
        if role == "user":
            lc_msgs.append(HumanMessage(content=content))
        elif role == "assistant":
            lc_msgs.append(AIMessage(content=content))
    return lc_msgs


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
    yield (str({"event": "start", "conversation_id": conv_id}) + "\n").encode("utf-8")
    try:
        config = {"configurable": {"thread_id": conv_id}}
        # Provide full conversation so the graph can avoid repeated asks
        lc_history = _to_lc_messages(conv)
        out = graph.invoke({"messages": lc_history}, config=config)
        # Emit one message event with assistant content
        msgs = out.get("messages") or []
        # The last message should be the assistant's reply
        text = ""
        if msgs and isinstance(msgs[-1], AIMessage):
            text = msgs[-1].content or ""
        else:
            # Fallback: search for last AI
            for m in reversed(msgs):
                if isinstance(m, AIMessage):
                    text = m.content or ""
                    break
        # Persist assistant reply into conversation history
        if text:
            import uuid as _uuid
            mid = str(_uuid.uuid4())
            MESSAGES[mid] = {"id": mid, "conv_id": conv_id, "role": "assistant", "content": text}
            CONVERSATIONS[conv_id]["messages"].append(mid)
        yield (str({"event": "message", "role": "assistant", "content": text}) + "\n").encode("utf-8")
        yield (str({"event": "done"}) + "\n").encode("utf-8")
    except Exception as e:
        yield (str({"event": "error", "message": str(e)}) + "\n").encode("utf-8")


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

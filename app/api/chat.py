from __future__ import annotations
import uuid
from typing import Iterator
import json

from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse

from ..services.conversation_repository import (
    append_message,
    ensure_conversation,
    get_last_user_message,
    get_messages,
    set_conversation_stopped,
    get_conversation_state,
    set_conversation_state,
)
from ..chatbot.graph import process_message


router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("/messages")
def post_message(payload: dict) -> dict:
    content = (payload or {}).get("content") or ""
    if not isinstance(content, str) or not content.strip():
        return {"error": "content is required"}
    conv_id = (payload or {}).get("conversation_id") or str(uuid.uuid4())
    ensure_conversation(conv_id)
    msg_id = str(uuid.uuid4())
    append_message(conv_id, msg_id, "user", content)
    return {
        "conversation_id": conv_id,
        "message_id": msg_id,
        "stream_url": f"/api/chat/stream/{conv_id}",
    }


def _stream_assistant(conv_id: str) -> Iterator[bytes]:
    user_msg = get_last_user_message(conv_id)
    if not user_msg:
        yield (json.dumps({"event": "error", "message": "No conversation or message found"}) + "\n").encode("utf-8")
        return

    yield (json.dumps({"event": "start", "conversation_id": conv_id}) + "\n").encode("utf-8")
    try:
        # Load previous state if any
        prev_state = get_conversation_state(conv_id) or {}
        # Also construct rolling history from stored messages (last 4)
        try:
            msgs = get_messages(conv_id)
            history = [
                {"role": m.get("role", "user"), "content": m.get("content", "")}
                for m in msgs if m.get("content") is not None
            ]
            # Keep last 4 messages to match state expectations
            if len(history) > 4:
                history = history[-4:]
            if isinstance(prev_state, dict):
                prev_state.setdefault("history", history)
            else:
                prev_state = {"history": history}
        except Exception:
            # Non-fatal if history cannot be built
            pass

        result = process_message(
            user_message=str(user_msg.get("content") or ""),
            previous_state=prev_state if isinstance(prev_state, dict) else None,
        )
        text = result.get("response") or ""
        yield (json.dumps({"event": "message", "role": "assistant", "content": text}) + "\n").encode("utf-8")
        if text:
            assistant_id = str(uuid.uuid4())
            append_message(conv_id, assistant_id, "assistant", text)
        # Persist updated state for future turns
        state_out = result.get("state")
        if isinstance(state_out, dict):
            set_conversation_state(conv_id, state_out)
        yield (json.dumps({"event": "done"}) + "\n").encode("utf-8")
    except Exception as e:
        yield (json.dumps({"event": "error", "message": str(e)}) + "\n").encode("utf-8")


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

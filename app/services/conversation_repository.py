from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from pymongo.collection import Collection

from .mongo import get_database
from . import store as memory_store


def _mongo_collections() -> tuple[Optional[Collection], Optional[Collection]]:
    db = get_database()
    if db is None:
        return None, None
    return db["conversations"], db["messages"]


def ensure_conversation(conv_id: str) -> None:
    conv_col, _ = _mongo_collections()
    if conv_col is not None:
        now = datetime.now(timezone.utc)
        conv_col.update_one(
            {"_id": conv_id},
            {
                "$setOnInsert": {
                    "created_at": now,
                    "updated_at": now,
                    "message_count": 0,
                }
            },
            upsert=True,
        )
        return
    convo = memory_store.CONVERSATIONS.setdefault(
        conv_id,
        {
            "id": conv_id,
            "messages": [],
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        },
    )


def append_message(
    conv_id: str,
    msg_id: str,
    role: str,
    content: Any,
    extra: Optional[Dict[str, Any]] = None,
) -> None:
    conv_col, msg_col = _mongo_collections()
    timestamp = datetime.now(timezone.utc)
    if msg_col is not None and conv_col is not None:
        msg_col.insert_one(
            {
                "_id": msg_id,
                "conversation_id": conv_id,
                "role": role,
                "content": content,
                "extra": extra or {},
                "created_at": timestamp,
            }
        )
        conv_col.update_one(
            {"_id": conv_id},
            {
                "$set": {
                    "updated_at": timestamp,
                    "last_role": role,
                },
                "$inc": {"message_count": 1},
                "$setOnInsert": {"created_at": timestamp},
            },
            upsert=True,
        )
        return

    convo = memory_store.CONVERSATIONS.setdefault(conv_id, {"id": conv_id, "messages": []})
    memory_store.MESSAGES[msg_id] = {
        "id": msg_id,
        "conv_id": conv_id,
        "role": role,
        "content": content,
        "extra": extra or {},
        "created_at": timestamp,
    }
    convo.setdefault("messages", []).append(msg_id)
    convo["updated_at"] = timestamp
    convo["last_role"] = role
    convo["message_count"] = convo.get("message_count", 0) + 1


def get_messages(conv_id: str) -> List[Dict[str, Any]]:
    _, msg_col = _mongo_collections()
    if msg_col is not None:
        docs = msg_col.find({"conversation_id": conv_id}).sort("created_at", 1)
        return [
            {
                "id": str(doc.get("_id")),
                "role": doc.get("role", "user"),
                "content": doc.get("content"),
                "extra": doc.get("extra", {}),
                "created_at": (doc.get("created_at") or datetime.now(timezone.utc)).isoformat(),
            }
            for doc in docs
        ]

    convo = memory_store.CONVERSATIONS.get(conv_id)
    if not convo:
        return []
    results: List[Dict[str, Any]] = []
    for mid in convo.get("messages", []):
        msg = memory_store.MESSAGES.get(mid)
        if not msg:
            continue
        results.append(
            {
                "id": msg.get("id", mid),
                "role": msg.get("role", "user"),
                "content": msg.get("content"),
                "extra": msg.get("extra", {}),
                "created_at": (msg.get("created_at") or datetime.now(timezone.utc)).isoformat(),
            }
        )
    return results


def get_last_user_message(conv_id: str) -> Optional[Dict[str, Any]]:
    _, msg_col = _mongo_collections()
    if msg_col is not None:
        doc = msg_col.find_one(
            {"conversation_id": conv_id, "role": "user"},
            sort=[("created_at", -1)],
        )
        if doc:
            return {
                "id": str(doc.get("_id")),
                "conversation_id": conv_id,
                "role": doc.get("role", "user"),
                "content": doc.get("content", ""),
                "extra": doc.get("extra", {}),
            }
        return None

    convo = memory_store.CONVERSATIONS.get(conv_id)
    if not convo:
        return None
    for msg_id in reversed(convo.get("messages", [])):
        msg = memory_store.MESSAGES.get(msg_id)
        if msg and msg.get("role") == "user":
            return msg
    return None


def set_conversation_stopped(conv_id: str, stopped: bool) -> None:
    conv_col, _ = _mongo_collections()
    if conv_col is not None:
        conv_col.update_one({"_id": conv_id}, {"$set": {"stopped": stopped}})
        return
    convo = memory_store.CONVERSATIONS.setdefault(conv_id, {"id": conv_id, "messages": []})
    convo["stopped"] = stopped

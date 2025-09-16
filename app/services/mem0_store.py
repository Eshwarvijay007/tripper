from __future__ import annotations

import logging
import os
from functools import lru_cache
from typing import Iterable, List, Optional

try:
    from mem0 import MemoryClient
except ImportError:  # pragma: no cover - mem0 optional in some environments
    MemoryClient = None  # type: ignore

logger = logging.getLogger(__name__)

_NOT_CONFIGURED_LOGGED = False


def _get_env(name: str) -> Optional[str]:
    value = os.getenv(name)
    if value:
        value = value.strip()
    return value or None


@lru_cache(maxsize=1)
def _get_client() -> Optional[MemoryClient]:
    """Create (and cache) a Mem0 client if configuration is available."""

    global _NOT_CONFIGURED_LOGGED

    if MemoryClient is None:
        if not _NOT_CONFIGURED_LOGGED:
            logger.info("mem0 package not available; skipping persistent memory integration")
            _NOT_CONFIGURED_LOGGED = True
        return None

    api_key = _get_env("MEM0_API_KEY")
    if not api_key:
        if not _NOT_CONFIGURED_LOGGED:
            logger.info("MEM0_API_KEY not configured; chat memory persistence disabled")
            _NOT_CONFIGURED_LOGGED = True
        return None

    host = _get_env("MEM0_API_URL") or _get_env("MEM0_HOST")
    org_id = _get_env("MEM0_ORG_ID")
    project_id = _get_env("MEM0_PROJECT_ID")

    client_kwargs = {"api_key": api_key}
    if host:
        client_kwargs["host"] = host.rstrip("/")
    if org_id and project_id:
        client_kwargs["org_id"] = org_id
        client_kwargs["project_id"] = project_id

    try:
        return MemoryClient(**client_kwargs)
    except Exception as exc:  # pragma: no cover - network/credentials issues
        logger.error("Failed to initialise Mem0 client: %s", exc)
        return None


def _normalise_memory_items(items: Iterable[dict]) -> List[str]:
    """Extract readable snippets from Mem0 search/get responses."""

    snippets: List[str] = []
    for item in items or []:
        if not isinstance(item, dict):
            continue
        text = (
            item.get("memory")
            or item.get("content")
            or item.get("text")
        )
        if text:
            snippets.append(str(text))
            continue

        messages = item.get("messages")
        if isinstance(messages, list):
            parts: List[str] = []
            for msg in messages:
                if not isinstance(msg, dict):
                    continue
                role = msg.get("role")
                content = msg.get("content")
                if not content:
                    continue
                if role:
                    parts.append(f"{role}: {content}")
                else:
                    parts.append(str(content))
            if parts:
                snippets.append("\n".join(parts))
    return snippets


def fetch_context(conversation_id: str, query: Optional[str] = None, *, limit: int = 5) -> List[str]:
    """Return previously stored memories for this conversation."""

    client = _get_client()
    if not client:
        return []

    try:
        k = max(1, min(int(limit or 5), 10))
        if query:
            results = client.search(query=query, user_id=conversation_id, top_k=k)
        else:
            results = client.get_all(version="v2", user_id=conversation_id, page_size=k)
    except Exception as exc:  # pragma: no cover - remote API failures
        logger.warning("Failed to fetch Mem0 context for %s: %s", conversation_id, exc)
        return []

    return _normalise_memory_items(results or [])

def record_user_message(conversation_id: str, content: str) -> None:
    """Persist a single user turn in Mem0."""

    if not content:
        return
    _store_messages(conversation_id, [{"role": "user", "content": content}])


def record_turn(conversation_id: str, user_text: Optional[str], assistant_text: Optional[str]) -> None:
    """Persist a user/assistant exchange for later retrieval."""

    messages = []
    if user_text:
        messages.append({"role": "user", "content": user_text})
    if assistant_text:
        messages.append({"role": "assistant", "content": assistant_text})
    if not messages:
        return
    _store_messages(conversation_id, messages)


def _store_messages(conversation_id: str, messages: List[dict]) -> None:
    client = _get_client()
    if not client:
        return
    try:
        client.add(
            messages,
            user_id=conversation_id,
            metadata={"conversation_id": conversation_id},
        )
    except Exception as exc:  # pragma: no cover - remote API failures
        logger.warning("Failed to persist Mem0 messages for %s: %s", conversation_id, exc)

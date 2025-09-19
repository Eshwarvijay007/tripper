import json
from typing import List, Tuple

from ..utils import get_text


_ORDERED_FIELDS: List[Tuple[str, str]] = [
    ("location", "destination"),
    ("trip_type", "trip type"),
    ("num_days", "number of days"),
    ("trip_start_day", "start date"),
    ("budget", "budget"),
]


def clarification_node(state, llm):
    """Ask for up to 3 missing preferences in a conversational way."""

    prefs = state.get("preferences", {}) or {}
    summary = state.get("summary", "")
    query = state.get("query", "")
    history = state.get("history") or []

    missing_fields = [(key, label) for key, label in _ORDERED_FIELDS if not prefs.get(key)]
    missing_labels = [label for key, label in missing_fields]
    state["missing_fields"] = missing_labels

    if not missing_fields:
        state["answer"] = None
        return state

    recent_turns = []
    for item in history[-4:]:
        role = item.get("role", "assistant")
        content = item.get("content", "")
        recent_turns.append(f"{role}: {content}")
    recent_context = "\n".join(recent_turns) if recent_turns else "None"

    prompt = f"""
You are Sunny, a cheerful and empathetic travel-planning assistant.

Context you can rely on:
- Current preference snapshot: {json.dumps(prefs, ensure_ascii=False)}
- All missing preference fields: {', '.join(missing_labels)}
- Last user message: {query}
- Conversation summary: {summary if summary else 'None provided'}
- Recent conversation turns:
{recent_context}

Your task:
1. Choose up to 3 of the most important missing fields to ask about based on conversation flow and what makes sense to ask together.
2. Ask for these details in a natural, conversational way that flows from the user's last message.
3. Keep your response to 2-3 sentences maximum, ending with a question.
4. For start date, mention that "flexible" is an acceptable answer.
5. Prioritize fields that are logically connected or build on each other.
6. Vary your tone and phrasing from previous turns.

Missing fields to choose from:
{chr(10).join([f"- {label}" for label in missing_labels])}

Examples of good groupings:
- Ask for destination + trip type together (they're related)
- Ask for number of days + start date together (scheduling related)
- Ask for budget along with other practical details

Craft a natural response that asks for the most logical 1-3 missing details now.
"""

    try:
        response = llm.invoke(prompt)
        state["answer"] = get_text(response).strip()
        if not state["answer"]:
            raise ValueError("Empty clarification response")
    except Exception as exc:
        print(f"Error in clarification node: {exc}")
        # Fallback to asking for the first missing field
        first_missing = missing_labels[0] if missing_labels else "details"
        state["answer"] = f"Could you share your {first_missing} so I can keep tailoring the plan?"

    return state
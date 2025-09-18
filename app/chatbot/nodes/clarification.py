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
    """Ask for the next missing preference in a conversational, varied way."""

    prefs = state.get("preferences", {}) or {}
    summary = state.get("summary", "")
    query = state.get("query", "")
    history = state.get("history") or []

    missing = [label for key, label in _ORDERED_FIELDS if not prefs.get(key)]
    state["missing_fields"] = missing

    if not missing:
        state["answer"] = None
        return state

    next_key, next_label = next(((k, l) for k, l in _ORDERED_FIELDS if not prefs.get(k)), (None, None))
    if not next_key:
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
- Current preference snapshot: {json.dumps(prefs, indent=2, ensure_ascii=False)}
- Missing preference labels (in order): {', '.join(missing)}
- Field you must ask for right now: {next_label}
- Last user message: {query}
- Conversation summary: {summary if summary else 'None provided'}
- Recent conversation turns:
{recent_context}

How to respond:
1. Start with a natural, human-sounding lead-in that connects with the user’s latest message or the plan so far.
2. Ask for the {next_label} specifically, and explain in a friendly way why you need it for the itinerary.
3. Keep the reply to one or two sentences. The last sentence must end with a question mark.
4. Mention that the start date can be "flexible" if {next_label} is the start date.
5. Do not mention any other missing fields; focus only on {next_label} right now.
6. Vary your tone and phrasing—do not reuse the same sentence structures from earlier turns or the examples below.

Inspiration only (do not copy):
- "Great, I’ve got the travel style noted. What city or region should I build the itinerary around?"
- "Thanks! To fine-tune the schedule, how many days do you want this trip to last?"
- "Wonderful choice so far; when would you like to set out? Saying \"flexible\" works too."

Craft your answer now.
"""

    try:
        response = llm.invoke(prompt)
        state["answer"] = get_text(response).strip()
        if not state["answer"]:
            raise ValueError("Empty clarification response")
    except Exception as exc:
        print(f"Error in clarification node: {exc}")
        fallback = "flexible" if next_key == "trip_start_day" else None
        if fallback == "flexible":
            state["answer"] = "I still need your start date—when would you like to begin, or is it flexible?"
        else:
            state["answer"] = f"Could you share your {next_label} so I can keep tailoring the plan?"

    return state

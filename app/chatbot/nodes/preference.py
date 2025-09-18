import json
import re
from typing import Any, Dict


def _extract_json_object(text: str) -> Dict[str, Any]:
    """Best-effort extraction of a JSON object from LLM text.
    Tries direct parse, fenced blocks, and brace-matching fallback.
    Returns {} on failure.
    """
    if not text:
        return {}
    # 1) direct
    try:
        return json.loads(text)
    except Exception:
        pass
    # 2) fenced ```json ... ``` or ``` ... ```
    fenced = re.search(r"```(?:json)?\s*([\s\S]*?)```", text, re.IGNORECASE)
    if fenced:
        inner = fenced.group(1).strip()
        try:
            return json.loads(inner)
        except Exception:
            pass
    # 3) brace matching: take first {...} block
    start = text.find('{')
    end = text.rfind('}')
    if start != -1 and end != -1 and end > start:
        candidate = text[start : end + 1]
        try:
            return json.loads(candidate)
        except Exception:
            pass
    return {}


def _normalize_prefs(prefs: Dict[str, Any]) -> Dict[str, Any]:
    # Map common synonyms
    mapping = {
        'destination': 'location',
        'city': 'location',
        'where': 'location',
        'days': 'num_days',
        'duration': 'num_days',
        'start_date': 'trip_start_day',
        'date': 'trip_start_day',
        'dates': 'trip_start_day',
        'type': 'trip_type',
    }
    out: Dict[str, Any] = {}
    for k, v in (prefs or {}).items():
        key = mapping.get(k, k)
        out[key] = v

    # Coerce num_days to int if possible
    if 'num_days' in out and out['num_days'] is not None:
        val = out['num_days']
        if isinstance(val, str):
            m = re.search(r"\d+", val)
            if m:
                out['num_days'] = int(m.group(0))
        elif isinstance(val, float):
            out['num_days'] = int(val)
    return out


def preference_node(state, llm):
    summary = state.get("summary", "")
    query = state.get("query", "")
    current_prefs = state.get("preferences", {})

    prompt = f"""
You are a preference extraction assistant for a trip planning chatbot.

Your task is to extract structured travel preferences from the conversation.

Current preferences already collected:
{json.dumps(current_prefs, indent=2)}

Required fields:
- location: The destination or city/country the user wants to visit (null if not mentioned).
- trip_type: Choose one or more from this list if mentioned, otherwise null:
  ["Adventure","Leisure","Business","Wellness","Cultural","Romantic","Family","Solo",
   "Friends/Group","Luxury","Budget/Backpacking","Eco/Nature","Spiritual/Pilgrimage",
   "Food & Wine","Festival/Event"]
- num_days: Number of days for the trip (integer, null if not specified).
- trip_start_day: Start date of the trip (YYYY-MM-DD format, null if not specified).
- budget: Budget amount with currency (e.g., "$1000", "€500", null if not specified).

Rules:
- Use both the conversation summary and the current user message.
- Only extract NEW or UPDATED information from the current message.
- If the user updates a detail, return the new value to overwrite the previous one.
- If a field is not mentioned in the current message, return null for that field.
- Return a valid JSON object only.

Conversation summary:
{summary}

Current user message:
{query}

Output format requirements:
- Return ONLY a JSON object, no markdown, no comments, no surrounding text.
- Include only fields that are NEW or UPDATED in the current message.
- Keys must be exactly: location, trip_type, num_days, trip_start_day, budget.
- Example: {{"location": "Paris", "num_days": 5}}

Now return the JSON object:
"""

    res = llm.invoke(prompt)

    # Parse response robustly
    raw = getattr(res, "content", "") or ""
    new_prefs = _extract_json_object(raw)
    new_prefs = _normalize_prefs(new_prefs)

    # Update preferences incrementally (dict-based)
    prefs = state.get("preferences") or {}
    if not isinstance(prefs, dict):
        prefs = {}
    for key, value in (new_prefs or {}).items():
        if value is not None:
            prefs[key] = value
    state["preferences"] = prefs
    
    # Check for missing required fields
    required_fields = ["location", "num_days", "trip_start_day"]
    missing = []
    for field in required_fields:
        if not prefs.get(field):
            missing.append(field)
    
    state["missing_fields"] = missing
    return state

import json
import re
from typing import Any, Dict
from ..utils import get_text


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
        'where': 'location',
        'duration': 'num_days',
        'start_date': 'trip_start_day',
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


def _extract_date_iso(text: str) -> str | None:
    """Extract a plausible start date in YYYY-MM-DD from free text.
    Prefers explicit ISO dates; supports MM/DD/YYYY and Month DD, YYYY.
    Returns None if nothing found.
    """
    if not text:
        return None
    # 1) ISO YYYY-MM-DD
    m = re.search(r"\b(19|20)\d{2}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])\b", text)
    if m:
        return m.group(0)
    # 2) MM/DD/YYYY or MM-DD-YYYY
    m = re.search(r"\b(0?[1-9]|1[0-2])[/-](0?[1-9]|[12]\d|3[01])[/-]((?:19|20)\d{2})\b", text)
    if m:
        mm = int(m.group(1)); dd = int(m.group(2)); yyyy = int(m.group(3))
        return f"{yyyy:04d}-{mm:02d}-{dd:02d}"
    # 3) Month name DD, YYYY
    months = {
        'jan': 1, 'january': 1,
        'feb': 2, 'february': 2,
        'mar': 3, 'march': 3,
        'apr': 4, 'april': 4,
        'may': 5,
        'jun': 6, 'june': 6,
        'jul': 7, 'july': 7,
        'aug': 8, 'august': 8,
        'sep': 9, 'sept': 9, 'september': 9,
        'oct': 10, 'october': 10,
        'nov': 11, 'november': 11,
        'dec': 12, 'december': 12,
    }
    m = re.search(r"\b([A-Za-z]{3,9})\s+(\d{1,2})(?:st|nd|rd|th)?(?:,)?\s+((?:19|20)\d{2})\b", text)
    if m:
        mon = months.get(m.group(1).lower())
        if mon:
            dd = int(m.group(2)); yyyy = int(m.group(3))
            return f"{yyyy:04d}-{mon:02d}-{dd:02d}"
    return None


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
- The object MUST have exactly these keys: location, trip_type, num_days, trip_start_day, budget.
- Use null for any field not mentioned in the CURRENT message.
 - Example: {{"location": "Paris", "trip_type": ["Cultural"], "num_days": 5, "trip_start_day": "2025-06-01", "budget": "$1500"}}

Now return the JSON object with exactly those five keys:
"""

    res = llm.invoke(prompt)

    # Parse response robustly
    raw = get_text(res)
    new_prefs = _extract_json_object(raw)
    new_prefs = _normalize_prefs(new_prefs)

    # Update preferences incrementally (dict-based)
    prefs = state.get("preferences") or {}
    if not isinstance(prefs, dict):
        prefs = {}
    for key, value in (new_prefs or {}).items():
        if value is not None:
            prefs[key] = value

    # Fallback: if trip_start_day missing in LLM output, try to parse it from the CURRENT user query
    if not prefs.get("trip_start_day"):
        date_from_query = _extract_date_iso(query)
        if date_from_query:
            prefs["trip_start_day"] = date_from_query

    state["preferences"] = prefs
    
    # Check for missing required fields
    required_fields = ["location", "num_days", "trip_start_day"]
    missing = []
    for field in required_fields:
        if not prefs.get(field):
            missing.append(field)
    
    state["missing_fields"] = missing
    return state

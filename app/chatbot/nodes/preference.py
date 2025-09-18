import json
from typing import Any, Dict

from ..utils import get_text


_ALLOWED_TRIP_TYPES = [
    "Adventure",
    "Leisure",
    "Business",
    "Wellness",
    "Cultural",
    "Romantic",
    "Family",
    "Solo",
    "Friends/Group",
    "Luxury",
    "Budget/Backpacking",
    "Eco/Nature",
    "Spiritual/Pilgrimage",
    "Food & Wine",
    "Festival/Event",
]

_EXPECTED_KEYS = {
    "location": None,
    "trip_type": None,
    "num_days": None,
    "trip_start_day": None,
    "budget": None,
}


def _extract_json_object(text: str) -> Dict[str, Any]:
    """Best-effort extraction of a JSON object from raw model output."""
    if not text:
        return {}
    try:
        return json.loads(text)
    except Exception:
        pass
    # Look for fenced code blocks
    fenced_start = text.lower().find("```json")
    if fenced_start != -1:
        fenced_start = text.find("\n", fenced_start)
        if fenced_start != -1:
            fenced_end = text.find("```", fenced_start + 1)
            if fenced_end != -1:
                snippet = text[fenced_start:fenced_end]
                try:
                    return json.loads(snippet)
                except Exception:
                    pass
    elif "```" in text:
        first = text.find("```")
        second = text.find("```", first + 3)
        if first != -1 and second != -1:
            snippet = text[first + 3:second]
            try:
                return json.loads(snippet)
            except Exception:
                pass
    # Fallback: first {...} block
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        snippet = text[start : end + 1]
        try:
            return json.loads(snippet)
        except Exception:
            pass
    return {}


def _normalise_result(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Coerce the parsed result into the expected preference schema."""
    if not isinstance(raw, dict):
        return dict(_EXPECTED_KEYS)

    # Allow the model to nest under a `preferences` key.
    if "preferences" in raw and isinstance(raw["preferences"], dict):
        raw = raw["preferences"]

    output: Dict[str, Any] = dict(_EXPECTED_KEYS)
    for key in _EXPECTED_KEYS:
        if key not in raw:
            continue
        value = raw[key]
        if key == "trip_type" and value is not None:
            if isinstance(value, str):
                value = [value.strip()] if value.strip() else None
            elif isinstance(value, list):
                cleaned = []
                for item in value:
                    if isinstance(item, str) and item.strip():
                        cleaned.append(item.strip())
                value = cleaned or None
        if key == "num_days" and value is not None:
            if isinstance(value, str) and value.strip().isdigit():
                value = int(value.strip())
            elif isinstance(value, (int, float)):
                value = int(value)
            else:
                value = None
        if key == "trip_start_day" and isinstance(value, str):
            value = value.strip()
            if not value:
                value = None
        if key == "budget" and isinstance(value, str):
            value = value.strip()
            if not value:
                value = None
        output[key] = value
    return output


def preference_node(state, llm):
    summary = state.get("summary", "")
    query = state.get("query", "")
    current_prefs = state.get("preferences", {}) or {}

    prompt = f"""
You manage preference gathering for a friendly travel-planning assistant.

Goal: read the conversation and output the up-to-date trip preferences using this schema:
- location: destination city/region/country (string)
- trip_type: array of labels from the allowed list (null if unknown)
- num_days: whole number of days (integer)
- trip_start_day: YYYY-MM-DD, or the string "flexible"
- budget: currency + amount (string)

Allowed trip_type values: {json.dumps(_ALLOWED_TRIP_TYPES)}

Follow these rules carefully:
1. Consider the stored preferences first. If the user did not change a field in the current message, copy the existing value.
2. If the user supplies new details or corrections in the current message, update that field accordingly.
3. When a field remains unknown after considering both the history and current message, return null for that field.
4. Normalise dates to YYYY-MM-DD when possible, convert written numbers into integers, and keep currencies with their symbols/codes.
5. If the user says their start date is flexible, set trip_start_day to "flexible".
6. Respond with JSON only. No extra prose, explanations, or markdown fences.

Stored preference snapshot:
{json.dumps(current_prefs, indent=2, ensure_ascii=False)}

Conversation summary:
{summary}

Current user message:
{query}

Return a JSON object with exactly these keys: location, trip_type, num_days, trip_start_day, budget.
"""

    try:
        raw_response = get_text(llm.invoke(prompt))
    except Exception as exc:
        print(f"Error calling preference LLM: {exc}")
        state["missing_fields"] = list(_EXPECTED_KEYS.keys())
        return state

    parsed = _extract_json_object(raw_response)
    new_prefs = _normalise_result(parsed)

    prefs = state.get("preferences")
    if not isinstance(prefs, dict):
        prefs = {}

    for key, value in new_prefs.items():
        if value is not None:
            prefs[key] = value

    state["preferences"] = prefs

    required_fields = list(_EXPECTED_KEYS.keys())
    missing = [field for field in required_fields if not prefs.get(field)]
    state["missing_fields"] = missing

    return state

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


# --- Heuristic fallback extractors (used when LLM JSON is missing) ---
_ALLOWED_TRIP_TYPES = [
    "Adventure","Leisure","Business","Wellness","Cultural","Romantic","Family","Solo",
    "Friends/Group","Luxury","Budget/Backpacking","Eco/Nature","Spiritual/Pilgrimage","Food & Wine","Festival/Event"
]

_TRIP_TYPE_SYNONYMS = {
    "backpacking": "Budget/Backpacking",
    "budget": "Budget/Backpacking",
    "cheap": "Budget/Backpacking",
    "food": "Food & Wine",
    "wine": "Food & Wine",
    "culinary": "Food & Wine",
    "gourmet": "Food & Wine",
    "hike": "Eco/Nature",
    "hiking": "Eco/Nature",
    "nature": "Eco/Nature",
    "outdoors": "Eco/Nature",
    "festival": "Festival/Event",
    "event": "Festival/Event",
    "pilgrimage": "Spiritual/Pilgrimage",
    "spiritual": "Spiritual/Pilgrimage",
    "temple": "Spiritual/Pilgrimage",
    "museum": "Cultural",
    "history": "Cultural",
    "cultural": "Cultural",
    "romantic": "Romantic",
    "honeymoon": "Romantic",
    "family": "Family",
    "kids": "Family",
    "solo": "Solo",
    "friends": "Friends/Group",
    "group": "Friends/Group",
    "luxury": "Luxury",
    "resort": "Luxury",
    "adventure": "Adventure",
    "business": "Business",
    "wellness": "Wellness",
    "spa": "Wellness",
    "relax": "Leisure",
    "leisure": "Leisure",
}

def _fallback_extract_trip_type(text: str) -> list | None:
    if not text:
        return None
    t = text.lower()
    found = []
    # Exact allowed labels
    for label in _ALLOWED_TRIP_TYPES:
        if label.lower() in t:
            found.append(label)
    # Synonyms
    for word, mapped in _TRIP_TYPE_SYNONYMS.items():
        if word in t and mapped not in found:
            found.append(mapped)
    return found or None

def _fallback_extract_num_days(text: str) -> int | None:
    if not text:
        return None
    # e.g., "5 days", "5-day", "for 5 days"
    m = re.search(r"\b(\d{1,3})\s*-(?:day|days)\b", text, re.IGNORECASE)
    if not m:
        m = re.search(r"\b(?:for\s+)?(\d{1,3})\s*(?:day|days)\b", text, re.IGNORECASE)
    if m:
        try:
            return int(m.group(1))
        except Exception:
            return None
    return None

def _fallback_extract_budget(text: str) -> str | None:
    if not text:
        return None
    # Match currency code or symbol + amount
    m = re.search(r"\b(?:USD|EUR|INR|GBP)\s*[\$€£₹]?\s*[0-9][0-9,]*(?:\.[0-9]{1,2})?\b", text, re.IGNORECASE)
    if not m:
        m = re.search(r"[\$€£₹]\s*[0-9][0-9,]*(?:\.[0-9]{1,2})?\b", text)
    if m:
        return m.group(0).strip()
    return None

def _fallback_extract_location(text: str) -> str | None:
    if not text:
        return None
    # Prefer "to <Place>" pattern
    m = re.search(r"\bto\s+([A-Z][A-Za-z\-'&\. ]{1,60})\b", text)
    if m:
        cand = m.group(1).strip()
        # Stop at common trailing terms
        cand = re.split(r"\s+(?:for|on|from|with|about|during|next|this|starting)\b", cand)[0].strip()
        return cand if cand else None
    # Fallback "in <Place>" but avoid months
    months = "jan feb mar apr may jun jul aug sep sept oct nov dec january february march april june july august september october november december".split()
    m = re.search(r"\bin\s+([A-Z][A-Za-z\-'&\. ]{1,60})\b", text)
    if m:
        cand = m.group(1).strip()
        first = cand.split()[0].lower()
        if first not in months:
            cand = re.split(r"\s+(?:for|on|from|with|about|during|next|this|starting)\b", cand)[0].strip()
            if cand:
                return cand
    # Last resort: any capitalized word sequence (likely a place)
    m = re.search(r"\b([A-Z][A-Za-z\-'&\.]+(?:\s+[A-Z][A-Za-z\-'&\.]+){0,3})\b", text)
    if m:
        return m.group(1).strip()
    return None

def _fallback_extract_from_text(text: str) -> Dict[str, Any]:
    out: Dict[str, Any] = {
        "location": None,
        "trip_type": None,
        "num_days": None,
        "trip_start_day": None,
        "budget": None,
    }
    if not text:
        return out
    # Date or flexible
    if "flexible" in text.lower():
        out["trip_start_day"] = "flexible"
    else:
        date = _extract_date_iso(text)
        if date:
            out["trip_start_day"] = date
    # Days
    nd = _fallback_extract_num_days(text)
    if nd:
        out["num_days"] = nd
    # Trip type
    tt = _fallback_extract_trip_type(text)
    if tt:
        out["trip_type"] = tt
    # Budget
    bg = _fallback_extract_budget(text)
    if bg:
        out["budget"] = bg
    # Location
    loc = _fallback_extract_location(text)
    if loc:
        out["location"] = loc
    return out


def preference_node(state, llm):
    summary = state.get("summary", "")
    query = state.get("query", "")
    current_prefs = state.get("preferences", {})

    prompt = f"""
You are a precise preference extraction assistant for a trip planning chatbot.

Goal: Extract only the NEW or CHANGED trip details from the user's CURRENT message, mapped to this fixed schema:
- location: Destination city/region/country (string) — null if not mentioned
- trip_type: One or more labels from the allowed list (array of strings) — null if not mentioned
- num_days: Whole number of trip days (integer) — null if not mentioned
- trip_start_day: Trip start date in YYYY-MM-DD (string) — if the user explicitly says "flexible", set this to "flexible"; otherwise null if not mentioned
- budget: Budget including currency symbol/code (string, e.g., "$1200", "€800", "INR 50,000") — null if not mentioned

Allowed trip_type values (use these labels exactly if applicable):
["Adventure","Leisure","Business","Wellness","Cultural","Romantic","Family","Solo",
 "Friends/Group","Luxury","Budget/Backpacking","Eco/Nature","Spiritual/Pilgrimage","Food & Wine","Festival/Event"]

Important rules:
- Consider BOTH the conversation summary and the CURRENT user message, but only emit fields that are explicitly present or updated in the CURRENT message.
- If the CURRENT message does not mention a field, set it to null (even if it appears in the summary).
- Normalize values when obvious: extract the number for num_days; convert dates like MM/DD/YYYY or "June 5, 2026" to YYYY-MM-DD; keep budget text with currency.
- If trip_type is a single value, you may return ["Leisure"] style array with one item.
- Return a VALID JSON object ONLY. No extra text or markdown.

Current preferences already collected (for your context; do NOT repeat unchanged values unless updated by the CURRENT message):
{json.dumps(current_prefs, indent=2)}

Conversation summary:
{summary}

Current user message:
{query}

Output requirements (strict):
- Return ONLY a JSON object with EXACTLY these keys: location, trip_type, num_days, trip_start_day, budget
- Use null for any key not present in the CURRENT message
- Example: {{"location": "Paris", "trip_type": ["Cultural"], "num_days": 5, "trip_start_day": "2025-06-01", "budget": "$1500"}}
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

    # If user explicitly said the date is flexible in the CURRENT message, record that
    if not new_prefs.get("trip_start_day") and isinstance(query, str) and "flexible" in query.lower():
        new_prefs["trip_start_day"] = "flexible"

    # Heuristic fallback when LLM didn't return parseable JSON
    if not new_prefs or all(new_prefs.get(k) in (None, []) for k in ["location","trip_type","num_days","trip_start_day","budget"]):
        heur = _fallback_extract_from_text(query or "")
        for k, v in heur.items():
            if v not in (None, []):
                new_prefs[k] = v
    for key, value in (new_prefs or {}).items():
        if value is not None:
            prefs[key] = value

    # Fallback: if trip_start_day missing in LLM output and not marked flexible, try to parse it from the CURRENT user query
    if not prefs.get("trip_start_day") or prefs.get("trip_start_day") in (None, ""):
        date_from_query = _extract_date_iso(query)
        if date_from_query:
            prefs["trip_start_day"] = date_from_query

    state["preferences"] = prefs
    
    # Check for missing fields in canonical order (ask one-by-one later)
    required_fields = [
        "location",
        "trip_type",
        "num_days",
        "trip_start_day",
        "budget",
    ]
    missing = []
    for field in required_fields:
        if not prefs.get(field):
            missing.append(field)
    
    state["missing_fields"] = missing
    return state

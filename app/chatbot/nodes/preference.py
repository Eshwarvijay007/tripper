import json

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

Return JSON with only the fields that need to be updated based on the current message:
"""

    res = llm.invoke(prompt)

    try:
        # Parse the response content as JSON
        new_prefs = json.loads(getattr(res, "content", "{}") or "{}")
    except Exception:
        # Fallback: empty dict means no updates
        new_prefs = {}

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

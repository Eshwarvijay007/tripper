def clarification_node(state, llm):
    """Ask for missing information one-by-one with a clear explanation."""

    prefs = state.get("preferences", {})

    # Determine missing fields in a fixed order
    ordered_fields = [
        ("location", "destination"),
        ("trip_type", "trip type"),
        ("num_days", "number of days"),
        ("trip_start_day", "start date"),
        ("budget", "budget"),
    ]
    missing = [label for key, label in ordered_fields if not prefs.get(key)]

    state["missing_fields"] = missing

    if missing:
        # Ask only for the NEXT missing field, and explain what's missing
        next_key, next_label = next(((k, l) for k, l in ordered_fields if not prefs.get(k)), (None, None))

        # Craft a focused, friendly prompt
        prompt = f"""
You are a warm, friendly travel planning assistant.

Context:
- Current trip preferences: {json.dumps(prefs)}
- Missing fields (in order): {', '.join(missing)}
- Ask ONLY for the next missing field: {next_label}

Your task:
- Ask one concise question (1 sentence) to collect the next missing field only: {next_label}.
- Clearly state what is missing so the user understands why you’re asking.
- If the missing field is the start date, mention they can say "flexible" if they aren’t sure.
- Do NOT ask about any other fields in this turn.

Guidance examples (adapt to the field):
- destination: "I’m missing your destination — where would you like to go?"
- trip type: "I’m missing your trip type (e.g., Leisure, Cultural); what kind of trip do you prefer?"
- number of days: "I’m missing the trip length — how many days are you planning?"
- start date: "I’m missing your start date — when would you like to begin? (You can say ‘flexible’.)"
- budget: "I’m missing your budget — roughly how much would you like to spend (include currency)?"

Now ask just one friendly question for: {next_label}
"""

        try:
            res = llm.invoke(prompt)
            state["answer"] = get_text(res).strip()
        except Exception as e:
            print(f"Error in clarification node: {e}")
            # Focused fallback
            state["answer"] = f"I’m missing your {next_label}. Could you share that?"

        return state

    # If nothing is missing, proceed without setting answer
    state["answer"] = None
    return state
from ..utils import get_text
import json

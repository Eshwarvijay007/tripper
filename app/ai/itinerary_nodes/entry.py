from __future__ import annotations
from app.ai.gemini import gemini_text
from .state import PlanState


def intent(state: PlanState) -> PlanState:
    '''Extract the user message and the summary and try to understand the intent of the user'''

    text = state.get("user_text") or ""
    short_term_memory = state.get("short_term_memory") or ""

    if not text.strip():
        state["intent"] = "unknown"
        state["next"] = "check_missing"
        return state

    # Build the prompt for intent classification
    prompt = f"""You are an intent classification assistant for a travel chatbot.
Your task is to classify the user's message into **one** of the following three categories:

- **trip_planning**: The user is asking about or trying to plan a trip (e.g., mentioning destinations, dates, travel preferences, activities).
- **small_talk**: The user is making casual conversation, greetings, or polite small talk.
- **unknown**: The message doesn't clearly belong to either of the above categories.

Only respond with **one label**, exactly as written: `trip_planning`, `small_talk`, or `unknown`.

---

**Examples:**
User: "Hi, how are you?" → `small_talk`
User: "I want to plan a trip to Italy next month." → `trip_planning`
User: "Tell me something interesting." → `unknown`
User: "Can you help me decide where to go for vacation?" → `trip_planning`
User: "What's your name?" → `small_talk`

---

{f"Previous conversation context: {short_term_memory}" if short_term_memory else ""}

Now classify the following user message:
User: "{text}" →"""

    try:
        intent_result = gemini_text(prompt, temperature=0.1).strip().lower()
        
        # Clean up the response and validate
        if "trip_planning" in intent_result:
            classified_intent = "trip_planning"
        elif "small_talk" in intent_result:
            classified_intent = "small_talk"
        else:
            classified_intent = "unknown"
            
        state["intent"] = classified_intent
        
        # Set next node based on intent
        if classified_intent == "trip_planning":
            state["next"] = "parse_intent"
        elif classified_intent == "small_talk":
            state["next"] = "small_talk_response"
        else:
            state["next"] = "unknown_response"
            
    except Exception as e:
        # Fallback to unknown on any error
        state["intent"] = "unknown"
        state["next"] = "unknown_response"
        state["error"] = f"Intent classification failed: {str(e)}"

    return state
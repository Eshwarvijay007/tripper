def intent_node(state, llm):
    """Classify user intent as trip planning or small talk"""
    
    summary = state.get("summary", "")
    query = state.get("query", "")

    prompt = f"""
You are an intent classification assistant for a travel chatbot.

Your job:
- Read the conversation summary and the user's current query.
- Decide if the user is asking about trip planning or just making small talk.
- Only output one label: `trip_planning` or `small_talk`.

Definitions:
- **trip_planning**: The user is asking about or trying to plan a trip (e.g., mentioning destinations, dates, travel preferences, activities, itinerary, budget, suggestions, asking for travel advice).
- **small_talk**: The user is making casual conversation, greetings, or polite chatter unrelated to trip planning.

Examples:
User: "Hi, how are you?" → `small_talk`
User: "I want to plan a trip to Italy next month." → `trip_planning`
User: "Tell me something interesting." → `small_talk`
User: "Can you help me decide where to go for vacation?" → `trip_planning`
User: "What's your name?" → `small_talk`
User: "I'm thinking of visiting Japan" → `trip_planning`
User: "Thanks for your help!" → `small_talk`
User: "What activities can I do in Paris?" → `trip_planning`

---

Conversation summary so far:
{summary}

Current user message:
{query}

Answer with exactly one label: `trip_planning` or `small_talk`
"""

    try:
        res = llm.invoke(prompt)
        intent = res.content.strip().lower()
        
        # Validate the response
        if intent in ["trip_planning", "small_talk"]:
            state["intent"] = intent
        else:
            # Default to trip_planning if unclear
            state["intent"] = "trip_planning"
            
    except Exception as e:
        print(f"Error in intent classification: {e}")
        # Default to trip_planning on error
        state["intent"] = "trip_planning"
    
    return state
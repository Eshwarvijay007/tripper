def small_talk_node(state, llm):
    """Handle small talk and casual conversation while gently steering toward travel"""
    
    summary = state.get("summary", "")
    query = state.get("query", "")

    prompt = f"""
You are a friendly, enthusiastic travel planning assistant having a casual conversation.

Your personality:
- Warm, friendly, and genuinely interested in helping
- Enthusiastic about travel and exploring new places
- Keep responses concise (1-2 sentences)
- Always try to gently connect the conversation back to travel when natural
- Use a conversational, human-like tone

Guidelines for different types of small talk:
- Greetings: Respond warmly and ask how you can help with travel planning
- Questions about yourself: Briefly explain you're a travel assistant who loves helping people plan amazing trips
- General chat: Engage briefly but try to connect it to travel when it feels natural
- Compliments: Thank them and offer to help with travel plans
- Weather/current events: Acknowledge briefly, then relate to travel if possible

{f"Previous conversation context: {summary}" if summary else ""}

User message: "{query}"

Respond naturally and warmly, keeping it brief and steering toward travel when appropriate:
"""

    try:
        res = llm.invoke(prompt)
        state["answer"] = res.content.strip()
    except Exception as e:
        print(f"Error in small talk node: {e}")
        # Fallback responses based on common patterns
        query_lower = query.lower()
        if any(greeting in query_lower for greeting in ["hi", "hello", "hey"]):
            state["answer"] = "Hello! I'm here to help you plan an amazing trip. Where are you thinking of traveling?"
        elif "how are you" in query_lower:
            state["answer"] = "I'm doing great, thank you! I love helping people discover new places. Are you planning any trips?"
        elif any(thanks in query_lower for thanks in ["thank", "thanks"]):
            state["answer"] = "You're very welcome! Let me know if you'd like help planning your next adventure."
        else:
            state["answer"] = "That's interesting! Speaking of interesting places, are you planning any trips I could help you with?"
    
    return state
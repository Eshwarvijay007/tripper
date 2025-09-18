
def summary_node(state, llm):
    query = state.get("query", "")
    summary = state.get("summary", "")
    history = state.get("history", [])[-4:]
    
    # Add current message to history
    if query:
        state.add_message_to_history("user", query)
    
    formatted_history = "\n".join(
        [f"{msg['role'].capitalize()}: {msg['content']}" for msg in history]
    )

    prompt = f"""
You are maintaining a running summary of a trip planning conversation.

Rules:
- Only include information that the user has actually provided.
- If the user changes a detail (e.g., new destination, new budget), update the summary and remove the old one.
- Keep the summary concise and factual, without conversational fluff.
- Include both trip-related information (destination, dates, budget, interests) and any relevant small talk context.
- If this is the first message, create a new summary.

Previous summary:
{summary}

New user message:
{query}

Conversation history (last 4 messages):
{formatted_history}

Return an updated summary in plain text.
"""

    res = llm.invoke(prompt)
    state["summary"] = res.content
    return state

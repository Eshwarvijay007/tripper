def clarification_node(state, llm):
    """Ask for missing required information in a conversational way"""
    
    prefs = state.get("preferences", {})
    missing = []

    # Check for required fields
    if not prefs.get("location"):
        missing.append("destination")
    if not prefs.get("num_days"):
        missing.append("number of days")
    if not prefs.get("trip_start_day"):
        missing.append("start date")

    state["missing_fields"] = missing

    if missing:
        # Create a natural, conversational prompt for asking missing info
        prompt = f"""
You are a warm, friendly travel planning assistant. The user wants to plan a trip but hasn't provided some key details yet.

Current trip preferences:
{prefs}

Missing information: {', '.join(missing)}

Your task:
- Ask for the missing information in a natural, conversational way
- Keep it concise (1-2 sentences max)
- Be encouraging and enthusiastic about helping them plan their trip
- If asking about dates, suggest they can be flexible if they prefer
- Make it feel like a helpful conversation, not an interrogation

Ask for the missing details in a friendly way:
"""

        try:
            res = llm.invoke(prompt)
            state["answer"] = get_text(res).strip()
        except Exception as e:
            print(f"Error in clarification node: {e}")
            # Fallback to simple message
            if len(missing) == 1:
                state["answer"] = f"I just need to know your {missing[0]} to help plan your perfect trip!"
            else:
                state["answer"] = f"I need a few more details: {', '.join(missing)}. Could you share those with me?"
        
        return state

    # If nothing is missing, proceed without setting answer
    state["answer"] = None
    return state
from ..utils import get_text

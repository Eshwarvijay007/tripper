from __future__ import annotations
from app.ai.gemini import gemini_text
from app.ai.memory import memory
from .state import PlanState


def node_small_talk(state: PlanState) -> PlanState:
    '''Handle small talk conversations with friendly, travel-focused responses'''
    
    text = state.get("user_text") or ""
    short_term_memory = state.get("short_term_memory") or ""
    
    if not text.strip():
        state["response"] = "Hello! I'm here to help you plan amazing trips. What can I do for you today?"
        return state
    
    # Build context-aware prompt for small talk
    context_prompt = f"""You are a friendly travel chatbot assistant. The user is making small talk or casual conversation.

Your personality:
- Warm, friendly, and enthusiastic about travel
- Helpful and encouraging
- Keep responses concise (1-2 sentences)
- Always try to gently steer the conversation toward travel if appropriate
- Use a conversational, human-like tone

Guidelines:
- For greetings: Respond warmly and ask how you can help with travel planning
- For questions about yourself: Briefly explain you're a travel planning assistant
- For general chat: Engage briefly but try to connect it to travel when natural
- For compliments: Thank them and offer to help with travel plans
- Keep responses short and engaging

{f"Previous conversation context: {short_term_memory}" if short_term_memory else ""}

User message: "{text}"

Respond naturally and warmly:"""

    try:
        response = gemini_text(context_prompt, temperature=0.7, max_output_tokens=150)
        
        # Clean up the response
        response = response.strip()
        if not response:
            response = "Thanks for chatting! I'm here whenever you're ready to plan your next adventure."
            
        state["response"] = response
        
        # Store the bot response in memory
        user_id = state.get("user_id", "anonymous")
        try:
            memory.add_chat(response, user_id=user_id, role="assistant")
        except Exception:
            pass  # Don't fail if memory storage fails
        
    except Exception as e:
        # Fallback response on error
        response = "Hello! I'm your travel planning assistant. How can I help you plan your next trip?"
        state["response"] = response
        state["error"] = f"Small talk generation failed: {str(e)}"
        
        # Store fallback response in memory too
        user_id = state.get("user_id", "anonymous")
        try:
            memory.add_chat(response, user_id=user_id, role="assistant")
        except Exception:
            pass
    
    return state
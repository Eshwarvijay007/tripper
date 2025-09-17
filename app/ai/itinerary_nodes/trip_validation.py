from __future__ import annotations
from typing import List, Dict, Any
from app.ai.gemini import gemini_text
from app.ai.memory import get_user_preferences
from .state import PlanState


def node_validate_trip_requirements(state: PlanState) -> PlanState:
    """
    Validate that essential trip planning information is available.
    Check current state and long-term memory for missing details.
    """
    
    user_id = state.get("user_id", "anonymous")
    questions: List[str] = []
    missing_fields: List[str] = []
    
    # Handle disambiguation first (existing logic)
    opts = state.get("disambiguate_options") or []
    if opts:
        name = (state.get("destinations") or [{}])[0].get("city") or "this place"
        labels = []
        for o in opts[:5]:
            city = o.get("city") or name
            country = o.get("country") or ""
            labels.append(f"{city}{(', ' + country) if country else ''}")
        questions.append(f"There are multiple places named '{name}'. Which one do you mean? " + ", ".join(labels) + ".")
        state["need_info"] = True
        state["questions"] = questions
        state["next"] = "finalize"
        return state

    # Get user preferences from memory to check what we already know
    try:
        user_prefs = get_user_preferences(user_id)
    except Exception:
        user_prefs = {"destinations": [], "budget": [], "activities": [], "accommodation": []}

    # Check essential fields
    missing_info = _check_essential_fields(state, user_prefs)
    
    if missing_info["missing_fields"]:
        # Generate contextual questions using AI
        questions = _generate_contextual_questions(
            state, 
            missing_info, 
            user_prefs,
            state.get("short_term_memory", "")
        )
        
        state["need_info"] = True
        state["questions"] = questions
        state["next"] = "finalize"
    else:
        state["need_info"] = False
        state["questions"] = []
        state["next"] = "enrich"
    
    return state


def _check_essential_fields(state: PlanState, user_prefs: Dict[str, Any]) -> Dict[str, Any]:
    """Check which essential fields are missing from state and memory"""
    
    missing_fields = []
    available_info = {}
    
    # Check destinations
    dests = state.get("destinations") or []
    memory_dests = [item.get('text', '') for item in user_prefs.get("destinations", [])]
    if not dests and not any("destination" in dest.lower() or "want to go" in dest.lower() for dest in memory_dests):
        missing_fields.append("destination")
    else:
        available_info["destination"] = dests or "from memory"
    
    # Check dates/duration
    dr = state.get("date_range")
    has_date_range = isinstance(dr, dict) and bool(dr.get("start")) and bool(dr.get("end"))
    
    nval = state.get("nights")
    try:
        nint = int(nval) if nval is not None else None
        if nint is not None and (nint < 1 or nint > 365):
            nint = None
    except Exception:
        nint = None
    
    has_nights = nint is not None
    
    if not has_date_range and not has_nights:
        missing_fields.append("dates_or_duration")
    else:
        available_info["dates_or_duration"] = "provided"
    
    # Check budget (new requirement)
    budget_info = state.get("budget") or state.get("currency")
    memory_budget = [item.get('text', '') for item in user_prefs.get("budget", [])]
    has_budget_info = budget_info or any("budget" in item.lower() or "spend" in item.lower() for item in memory_budget)
    
    if not has_budget_info:
        missing_fields.append("budget")
    else:
        available_info["budget"] = budget_info or "from memory"
    
    # Check origin (helpful but not always required)
    origin = state.get("origin")
    if not origin:
        # Check if we can infer from memory
        memory_origins = [item.get('text', '') for item in user_prefs.get("destinations", [])]
        has_origin_info = any("from" in item.lower() or "live in" in item.lower() for item in memory_origins)
        if not has_origin_info:
            missing_fields.append("origin")
    else:
        available_info["origin"] = origin
    
    return {
        "missing_fields": missing_fields,
        "available_info": available_info
    }


def _generate_contextual_questions(state: PlanState, missing_info: Dict, user_prefs: Dict, context: str) -> List[str]:
    """Generate contextual questions for missing information using AI"""
    
    missing_fields = missing_info["missing_fields"]
    available_info = missing_info["available_info"]
    user_text = state.get("user_text", "")
    
    # Build context for question generation
    prompt = f"""You are a helpful travel planning assistant. The user wants to plan a trip but some essential information is missing.

User's message: "{user_text}"

{f"Previous context: {context}" if context else ""}

Available information:
{chr(10).join([f"- {k}: {v}" for k, v in available_info.items()]) if available_info else "- None"}

Missing information needed: {', '.join(missing_fields)}

Generate 1-3 friendly, conversational questions to gather the missing information. Make the questions:
1. Natural and conversational (not robotic)
2. Specific to what's missing
3. Helpful by providing examples when appropriate
4. Considerate of what information is already available

For missing fields:
- destination: Ask where they want to go
- dates_or_duration: Ask for travel dates or trip duration
- budget: Ask about budget range or spending preferences
- origin: Ask where they're traveling from

Return only the questions, one per line, without numbering or bullets."""

    try:
        response = gemini_text(prompt, temperature=0.7, max_output_tokens=300)
        questions = [q.strip() for q in response.split('\n') if q.strip()]
        
        # Fallback to default questions if AI fails
        if not questions:
            questions = _get_default_questions(missing_fields)
            
        return questions[:3]  # Limit to 3 questions max
        
    except Exception:
        # Fallback to default questions
        return _get_default_questions(missing_fields)


def _get_default_questions(missing_fields: List[str]) -> List[str]:
    """Fallback default questions for missing fields"""
    
    question_map = {
        "destination": "Where would you like to go?",
        "dates_or_duration": "What are your travel dates, or how many nights would you like to stay?",
        "budget": "What's your budget range for this trip? (e.g., budget-friendly, mid-range, or luxury)",
        "origin": "Where will you be traveling from?"
    }
    
    return [question_map.get(field, f"Could you provide information about {field}?") for field in missing_fields]
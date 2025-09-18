import json
import re
from ..utils import get_text
from ...services.trip_suggestions import get_trip_plan_suggestions

def itinerary_node(state, llm):
    """Generate trip itinerary based on collected preferences"""
    
    # Extract preferences from state
    preferences = state.get("preferences", {})
    location = preferences.get("location")
    num_days = preferences.get("num_days")  # Fixed field name consistency
    trip_type = preferences.get("trip_type")
    budget = preferences.get("budget")
    trip_start_day = preferences.get("trip_start_day")

    # Check if we have minimum required information
    if not location or not num_days:
        state["answer"] = (
            "I need a bit more information to create your itinerary. "
            "Could you please provide the destination and number of days for your trip?"
        )
        return state

    # Normalize/parse values
    try:
        # num_days should be int
        if isinstance(num_days, str):
            m = re.search(r"\d+", num_days)
            if m:
                num_days = int(m.group(0))
        elif isinstance(num_days, float):
            num_days = int(num_days)

        # trip_type can be list from preference extraction; pick first if list
        if isinstance(trip_type, list) and trip_type:
            trip_type = trip_type[0]
        if not isinstance(trip_type, str) or not trip_type:
            trip_type = "Leisure"

        # budget may be like "$1500" or "€500" or number; extract digits
        budget_value = None
        if isinstance(budget, (int, float)):
            budget_value = float(budget)
        elif isinstance(budget, str):
            num = re.findall(r"[\d\.]+", budget)
            if num:
                try:
                    budget_value = float(num[0])
                except Exception:
                    budget_value = None
    except Exception:
        # Non-fatal normalization errors
        budget_value = None

    # Call trip suggestion service for a structured plan
    try:
        resp = get_trip_plan_suggestions(
            location=location,
            no_of_days_to_stay=int(num_days),
            trip_type=str(trip_type),
            budget=budget_value,
            language="en",
            region="IN",
        )

        # Store raw plan for frontend consumption
        state["trip_plan"] = resp

        # Compose a concise answer for chat
        trip_days = resp.get("trip_plan") or []
        stay_plan = resp.get("stay_plan") or []
        intro = f"I’ve prepared a {num_days}-day plan for {location}."
        day1_preview = ""
        if trip_days:
            first_day = trip_days[0]
            locs = first_day.get("locations") or []
            if locs:
                names = ", ".join([l.get("name", "") for l in locs[:3] if l.get("name")])
                if names:
                    day1_preview = f" Day 1 highlights: {names}."
        stays_preview = f" I also included {len(stay_plan)} stay options." if stay_plan else ""

        state["answer"] = (intro + day1_preview + stays_preview).strip()
        state["itinerary_done"] = True
        state["final_output"] = {
            "preferences": preferences,
            "generated_at": trip_start_day or "flexible",
            "trip_plan": resp,
        }

    except Exception as e:
        # Fallback to LLM text itinerary if service fails for any reason
        print(f"Error generating structured trip plan: {e}")
        prompt = f"""
You are an expert travel planner creating a detailed itinerary.

Trip Details:
- Destination: {location}
- Duration: {num_days} days
- Trip Type: {trip_type}
- Budget: {budget or 'Not specified'}
- Start Date: {trip_start_day or 'Flexible'}

Create a day-by-day itinerary that includes:
1. A warm, engaging introduction
2. Daily activities with specific recommendations
3. Estimated time for each activity
4. Brief descriptions of attractions/places
5. Practical tips (transportation, timing, etc.)
6. An encouraging closing message

Format as a clear, easy-to-read itinerary. Be enthusiastic and helpful!
"""
        try:
            res = llm.invoke(prompt)
            itinerary_text = get_text(res).strip()
            state["answer"] = itinerary_text
            state["itinerary_done"] = True
            state["final_output"] = {
                "itinerary": itinerary_text,
                "preferences": preferences,
                "generated_at": trip_start_day or "flexible",
            }
        except Exception as ee:
            print(f"Error generating fallback itinerary: {ee}")
            state["answer"] = (
                "I'm having trouble generating your itinerary right now. "
                "Could you confirm your destination and trip duration?"
            )
    
    return state

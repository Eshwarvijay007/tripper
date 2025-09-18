import json
from ..utils import get_text

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

    # For now, generate a sample itinerary using LLM
    # TODO: Replace with actual trip planning service call
    # resp = get_trip_plan_suggestions(
    #     location=location,
    #     no_of_days_to_stay=num_days,
    #     trip_type=trip_type,
    #     language="en",
    #     region="IN", 
    # )

    # Create a structured prompt for the LLM to generate itinerary
    prompt = f"""
You are an expert travel planner creating a detailed itinerary.

Trip Details:
- Destination: {location}
- Duration: {num_days} days
- Trip Type: {trip_type or 'General sightseeing'}
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
        
        # Save both the generated itinerary and mark as complete
        state["answer"] = itinerary_text
        state["itinerary_done"] = True
        state["final_output"] = {
            "itinerary": itinerary_text,
            "preferences": preferences,
            "generated_at": trip_start_day or "flexible"
        }

        #here we have to make proper object that should go to frontend
        
    except Exception as e:
        print(f"Error generating itinerary: {e}")
        state["answer"] = (
            "I'm having trouble generating your itinerary right now. "
            "Let me try again - could you confirm your destination and trip duration?"
        )
    
    return state

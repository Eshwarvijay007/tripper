import os
from mem0 import Memory

memory = Memory.from_config({
    "storage": {
        "type": "managed",
        "config": {
            "api_key": os.getenv("MEM0_API_KEY")
        }
    },
    "extraction": {
        "enabled": True,
        "schema": {
            "personal_info": [
                "name (string)",
                "age_group (child, teen, young_adult, adult, senior)",
                "nationality (string)",
                "languages_spoken (list of strings)",
                "accessibility_needs (list of strings)"
            ],
            "travel_preferences": [
                "preferred_origin (city, country)",
                "favorite_destinations (list of cities/countries)",
                "avoided_destinations (list of cities/countries with reasons)",
                "preferred_travel_seasons (spring, summer, fall, winter)",
                "preferred_trip_duration (1-30 days)",
                "typical_budget_range (budget, mid-range, luxury)",
                "currency_preference (USD, EUR, GBP, etc.)",
                "pace_preference (relaxed, moderate, busy, adventure)"
            ],
            "accommodation_preferences": [
                "accommodation_types (hotel, hostel, airbnb, resort, boutique)",
                "room_preferences (single, double, suite, family_room)",
                "amenity_preferences (pool, gym, spa, wifi, breakfast)",
                "location_preferences (city_center, beach, mountains, countryside)"
            ],
            "activity_interests": [
                "activity_types (cultural, adventure, relaxation, nightlife, shopping, food)",
                "specific_interests (museums, hiking, beaches, festivals, local_cuisine)",
                "physical_activity_level (low, moderate, high)",
                "cultural_interests (history, art, music, local_traditions)",
                "food_preferences (vegetarian, vegan, halal, kosher, allergies)"
            ],
            "travel_companions": [
                "typical_travel_style (solo, couple, family, friends, business)",
                "group_size_preference (1-10+ people)",
                "traveling_with_children (ages if applicable)",
                "traveling_with_pets (type of pets)"
            ],
            "transportation_preferences": [
                "preferred_flight_class (economy, business, first)",
                "airline_preferences (specific airlines or alliances)",
                "ground_transport_preferences (rental_car, public_transport, taxi, walking)",
                "mobility_requirements (wheelchair, assistance_needed)"
            ],
            "past_experiences": [
                "visited_destinations (list with satisfaction ratings)",
                "memorable_experiences (positive and negative)",
                "travel_mistakes_to_avoid (lessons_learned)",
                "recommended_places (with reasons)"
            ]
        },
        "prompt": """
You are an advanced travel preference extraction assistant. Analyze the user's message and extract detailed travel-related information across multiple categories.

Extract information for these categories ONLY if explicitly mentioned or strongly implied:

PERSONAL INFO: name, age_group, nationality, languages_spoken, accessibility_needs
TRAVEL PREFERENCES: preferred_origin, favorite_destinations, avoided_destinations, preferred_travel_seasons, preferred_trip_duration, typical_budget_range, currency_preference, pace_preference  
ACCOMMODATION: accommodation_types, room_preferences, amenity_preferences, location_preferences
ACTIVITIES: activity_types, specific_interests, physical_activity_level, cultural_interests, food_preferences
COMPANIONS: typical_travel_style, group_size_preference, traveling_with_children, traveling_with_pets
TRANSPORTATION: preferred_flight_class, airline_preferences, ground_transport_preferences, mobility_requirements
PAST EXPERIENCES: visited_destinations, memorable_experiences, travel_mistakes_to_avoid, recommended_places

IMPORTANT RULES:
- Only extract information that is clearly stated or strongly implied
- For dates, use format 'YYYY-MM-DD to YYYY-MM-DD' or 'YYYY-MM-DD' for single dates
- For duration, provide integer between 1-30 for days
- For lists, always return as arrays even for single items
- For budget, categorize as: budget, mid-range, luxury
- If information is uncertain, don't extract it
- Return valid JSON with only the categories that have extracted information

Return the extracted information as a clean JSON object with category names as keys.
        """
    }
})


def build_context(user_id, new_message, role="user"):
    """
    Build comprehensive context for the user including recent conversations and preferences.
    
    Args:
        user_id: Unique identifier for the user
        new_message: The current message from the user
        role: Role of the message sender (user/assistant)
    
    Returns:
        Dict with short_term, long_term, and formatted context
    """
    try:
        # Store current message in memory
        memory.add_chat(new_message, user_id=user_id, role=role)
        memory.add(new_message, user_id=user_id)

        # Retrieve recent conversation history (episodic memory)
        short_term = memory.search("Recent conversation history", user_id=user_id, limit=8)

        # Retrieve user preferences and facts (semantic memory)
        travel_prefs = memory.search("travel preferences and requirements", user_id=user_id, limit=10)
        personal_info = memory.search("personal information and constraints", user_id=user_id, limit=5)
        past_trips = memory.search("past travel experiences and feedback", user_id=user_id, limit=5)

        # Format context for better AI consumption
        formatted_context = _format_memory_context(short_term, travel_prefs, personal_info, past_trips)

        return {
            "short_term": short_term,
            "long_term": {
                "travel_preferences": travel_prefs,
                "personal_info": personal_info, 
                "past_experiences": past_trips
            },
            "formatted_context": formatted_context
        }
    
    except Exception as e:
        # Return empty context if memory system fails
        print(f"Memory context building failed: {e}")
        return {
            "short_term": [],
            "long_term": {"travel_preferences": [], "personal_info": [], "past_experiences": []},
            "formatted_context": ""
        }


def _format_memory_context(short_term, travel_prefs, personal_info, past_trips):
    """Format memory items into readable context for AI models"""
    context_parts = []
    
    # Recent conversation
    if short_term:
        recent_items = [item.get('text', item.get('memory', '')) for item in short_term[:3]]
        recent_items = [item for item in recent_items if item.strip()]
        if recent_items:
            context_parts.append("Recent conversation:\n" + "\n".join(f"- {item}" for item in recent_items))
    
    # Travel preferences
    if travel_prefs:
        pref_items = [item.get('text', item.get('memory', '')) for item in travel_prefs[:5]]
        pref_items = [item for item in pref_items if item.strip()]
        if pref_items:
            context_parts.append("Travel preferences:\n" + "\n".join(f"- {item}" for item in pref_items))
    
    # Personal constraints
    if personal_info:
        info_items = [item.get('text', item.get('memory', '')) for item in personal_info[:3]]
        info_items = [item for item in info_items if item.strip()]
        if info_items:
            context_parts.append("Personal info:\n" + "\n".join(f"- {item}" for item in info_items))
    
    # Past experiences
    if past_trips:
        trip_items = [item.get('text', item.get('memory', '')) for item in past_trips[:3]]
        trip_items = [item for item in trip_items if item.strip()]
        if trip_items:
            context_parts.append("Past experiences:\n" + "\n".join(f"- {item}" for item in trip_items))
    
    return "\n\n".join(context_parts)


def get_user_preferences(user_id):
    """Get structured user preferences for trip planning"""
    try:
        # Search for specific preference categories
        destinations = memory.search("favorite destinations and places to visit", user_id=user_id, limit=5)
        budget_prefs = memory.search("budget preferences and spending habits", user_id=user_id, limit=3)
        activity_prefs = memory.search("activity preferences and interests", user_id=user_id, limit=5)
        accommodation_prefs = memory.search("accommodation and hotel preferences", user_id=user_id, limit=3)
        
        return {
            "destinations": destinations,
            "budget": budget_prefs,
            "activities": activity_prefs,
            "accommodation": accommodation_prefs
        }
    except Exception as e:
        print(f"Failed to get user preferences: {e}")
        return {"destinations": [], "budget": [], "activities": [], "accommodation": []}


def populate_state_from_memory(user_id, current_state):
    """
    Populate state with structured data from memory if not already present.
    This reduces redundant questions by using known user preferences.
    
    Args:
        user_id: User identifier
        current_state: Current state dict to update
        
    Returns:
        Updated state dict with memory-based defaults
    """
    try:
        # Method 1: Try to get structured data from mem0's extraction
        structured_prefs = _get_structured_from_mem0(user_id)
        
        # Method 2: Fallback to manual extraction from memory text
        if not structured_prefs:
            all_memories = memory.get_all(user_id=user_id)
            structured_prefs = _extract_structured_preferences(all_memories)
        
        # Update state with memory data (only if not already present)
        updated_state = dict(current_state)
        
        # Origin - use preferred origin or last mentioned origin
        if not updated_state.get("origin") and structured_prefs.get("origin"):
            updated_state["origin"] = structured_prefs["origin"]
        
        # Currency preference
        if not updated_state.get("currency") and structured_prefs.get("currency"):
            updated_state["currency"] = structured_prefs["currency"]
            
        # Budget preference
        if not updated_state.get("budget") and structured_prefs.get("budget"):
            updated_state["budget"] = structured_prefs["budget"]
            
        # Interests - merge with existing
        memory_interests = structured_prefs.get("interests", [])
        current_interests = updated_state.get("interests", [])
        if memory_interests and not current_interests:
            updated_state["interests"] = memory_interests
        elif memory_interests and current_interests:
            # Merge unique interests
            all_interests = list(set(current_interests + memory_interests))
            updated_state["interests"] = all_interests
            
        # Pace preference
        if not updated_state.get("pace") and structured_prefs.get("pace"):
            updated_state["pace"] = structured_prefs["pace"]
            
        # Travel companions info
        if not updated_state.get("with_kids") and structured_prefs.get("with_kids") is not None:
            updated_state["with_kids"] = structured_prefs["with_kids"]
            
        # Must do activities from past preferences
        memory_must_do = structured_prefs.get("must_do", [])
        current_must_do = updated_state.get("must_do", [])
        if memory_must_do and not current_must_do:
            updated_state["must_do"] = memory_must_do
            
        # Things to avoid from past experiences
        memory_avoid = structured_prefs.get("avoid", [])
        current_avoid = updated_state.get("avoid", [])
        if memory_avoid and not current_avoid:
            updated_state["avoid"] = memory_avoid
            
        return updated_state
        
    except Exception as e:
        print(f"Failed to populate state from memory: {e}")
        return current_state


def _get_structured_from_mem0(user_id):
    """
    Try to get structured preferences directly from mem0's extraction capabilities
    """
    try:
        # Search for structured travel preferences
        travel_data = memory.search("user travel preferences and requirements", user_id=user_id, limit=10)
        
        structured_prefs = {
            "origin": None,
            "currency": None,
            "budget": None,
            "interests": [],
            "pace": None,
            "with_kids": None,
            "must_do": [],
            "avoid": []
        }
        
        # Process memory items that might contain structured data
        for item in travel_data:
            memory_text = item.get('text', item.get('memory', ''))
            
            # Look for structured data patterns that mem0 might have extracted
            if 'origin:' in memory_text.lower():
                origin_match = memory_text.lower().split('origin:')[1].split(',')[0].strip()
                if origin_match:
                    structured_prefs["origin"] = {"city": origin_match.title()}
                    
            if 'currency:' in memory_text.lower():
                currency_match = memory_text.lower().split('currency:')[1].split(',')[0].strip()
                if currency_match and len(currency_match) <= 3:
                    structured_prefs["currency"] = currency_match.upper()
                    
            if 'budget:' in memory_text.lower():
                budget_match = memory_text.lower().split('budget:')[1].split(',')[0].strip()
                if budget_match:
                    structured_prefs["budget"] = budget_match
                    
            if 'interests:' in memory_text.lower():
                interests_part = memory_text.lower().split('interests:')[1].split('.')[0]
                interests = [i.strip() for i in interests_part.split(',') if i.strip()]
                structured_prefs["interests"].extend(interests)
                
            if 'pace:' in memory_text.lower():
                pace_match = memory_text.lower().split('pace:')[1].split(',')[0].strip()
                if pace_match in ['relaxed', 'moderate', 'busy', 'packed']:
                    structured_prefs["pace"] = pace_match
        
        # Clean up and return
        structured_prefs["interests"] = list(set(structured_prefs["interests"]))[:5]
        return structured_prefs if any(structured_prefs.values()) else None
        
    except Exception as e:
        print(f"Failed to get structured data from mem0: {e}")
        return None


def _extract_structured_preferences(memories):
    """Extract structured preferences from memory items"""
    prefs = {
        "origin": None,
        "currency": None,
        "budget": None,
        "interests": [],
        "pace": None,
        "with_kids": None,
        "must_do": [],
        "avoid": []
    }
    
    if not memories:
        return prefs
        
    try:
        for memory_item in memories:
            memory_text = memory_item.get('text', memory_item.get('memory', '')).lower()
            
            # Extract origin/home location
            if any(phrase in memory_text for phrase in ['live in', 'from', 'based in', 'home is']):
                # Simple extraction - could be enhanced with NLP
                if 'live in' in memory_text:
                    origin_part = memory_text.split('live in')[1].split(',')[0].split('.')[0].strip()
                    if origin_part and len(origin_part) < 50:  # Reasonable city name length
                        prefs["origin"] = {"city": origin_part.title()}
                        
            # Extract currency preference
            currencies = ['usd', 'eur', 'gbp', 'inr', 'cad', 'aud', 'jpy']
            for curr in currencies:
                if curr in memory_text:
                    prefs["currency"] = curr.upper()
                    break
                    
            # Extract budget preference
            if any(phrase in memory_text for phrase in ['budget', 'cheap', 'affordable']):
                prefs["budget"] = "budget"
            elif any(phrase in memory_text for phrase in ['luxury', 'expensive', 'high-end', 'premium']):
                prefs["budget"] = "luxury"
            elif any(phrase in memory_text for phrase in ['mid-range', 'moderate', 'medium']):
                prefs["budget"] = "mid-range"
                
            # Extract interests
            interest_keywords = {
                'cultural': ['culture', 'museum', 'history', 'art', 'heritage'],
                'adventure': ['adventure', 'hiking', 'climbing', 'extreme'],
                'relaxation': ['relax', 'spa', 'beach', 'peaceful'],
                'food': ['food', 'cuisine', 'restaurant', 'culinary'],
                'nightlife': ['nightlife', 'bars', 'clubs', 'party'],
                'nature': ['nature', 'wildlife', 'national park', 'outdoors'],
                'shopping': ['shopping', 'markets', 'boutique']
            }
            
            for interest, keywords in interest_keywords.items():
                if any(keyword in memory_text for keyword in keywords):
                    if interest not in prefs["interests"]:
                        prefs["interests"].append(interest)
                        
            # Extract pace preference
            if any(phrase in memory_text for phrase in ['relaxed', 'slow', 'leisurely']):
                prefs["pace"] = "relaxed"
            elif any(phrase in memory_text for phrase in ['busy', 'packed', 'active']):
                prefs["pace"] = "packed"
                
            # Extract family travel info
            if any(phrase in memory_text for phrase in ['with kids', 'children', 'family trip']):
                prefs["with_kids"] = True
            elif any(phrase in memory_text for phrase in ['no kids', 'adults only', 'couple trip']):
                prefs["with_kids"] = False
                
            # Extract must-do preferences
            if 'must see' in memory_text or 'must do' in memory_text:
                # Extract the activity mentioned
                must_do_part = memory_text.split('must')[1].split('.')[0].strip()
                if must_do_part and len(must_do_part) < 100:
                    prefs["must_do"].append(must_do_part)
                    
            # Extract things to avoid
            if any(phrase in memory_text for phrase in ['avoid', 'don\'t like', 'hate', 'dislike']):
                avoid_part = memory_text.split('avoid')[0] if 'avoid' in memory_text else memory_text
                if len(avoid_part) < 100:
                    prefs["avoid"].append(avoid_part.strip())
                    
    except Exception as e:
        print(f"Error extracting structured preferences: {e}")
        
    # Clean up empty lists
    prefs["interests"] = [i for i in prefs["interests"] if i][:5]  # Limit to 5 interests
    prefs["must_do"] = [m for m in prefs["must_do"] if m][:3]  # Limit to 3 must-dos
    prefs["avoid"] = [a for a in prefs["avoid"] if a][:3]  # Limit to 3 avoids
    
    return prefs


def store_trip_feedback(user_id, trip_data, feedback):
    """Store feedback about completed trips for future reference"""
    try:
        feedback_message = f"Trip feedback: {trip_data.get('destination', 'Unknown destination')} - {feedback}"
        memory.add(feedback_message, user_id=user_id)
        return True
    except Exception as e:
        print(f"Failed to store trip feedback: {e}")
        return False

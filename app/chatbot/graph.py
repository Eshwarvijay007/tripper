from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from nodes.summary_node import summary_node
from nodes.intent import intent_node
from nodes.preference import preference_node
from nodes.itinerary_node import itinerary_node
from nodes.small_talk import small_talk_node
from nodes.clarification import clarification_node
from state import TripState

# Initialize Gemini LLM using langchain_google_genai
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.7,
    convert_system_message_to_human=True
)

#TODO:
    # Might need to add with structured output with the some node if the response is not good of gemini api
    # Final improvement of itineray node payload

# Error handling wrapper for nodes
def safe_node_wrapper(node_func, node_name):
    """Wrapper to add error handling to nodes"""
    def wrapper(state):
        try:
            return node_func(state, llm)
        except Exception as e:
            print(f"Error in {node_name}: {str(e)}")
            # Return state unchanged on error
            state["answer"] = f"I encountered an error while processing. Please try again."
            return state
    return wrapper

# Create the graph
graph = StateGraph(TripState)

# Add nodes with error handling
graph.add_node("summary", safe_node_wrapper(summary_node, "summary"))
graph.add_node("intent", safe_node_wrapper(intent_node, "intent"))
graph.add_node("small_talk", safe_node_wrapper(small_talk_node, "small_talk"))
graph.add_node("preferences", safe_node_wrapper(preference_node, "preferences"))
graph.add_node("clarification", safe_node_wrapper(clarification_node, "clarification"))
graph.add_node("itinerary", safe_node_wrapper(itinerary_node, "itinerary"))

# Set entry point
graph.set_entry_point("summary")

# Edges
graph.add_edge("summary", "intent")

# Route based on intent with fallback
def route_intent(state: TripState):
    intent = state.get("intent", "").lower()
    if intent == "small_talk":
        return "small_talk"
    elif intent in ["trip_planning"]:
        return "preferences"
    else:
        # Default to preferences for ambiguous cases
        return "preferences"

graph.add_conditional_edges("intent", route_intent)

# Preferences → Clarification
graph.add_edge("preferences", "clarification")

# Clarification → either end (to ask user) or go to itinerary
def route_clarification(state: TripState):
    missing_fields = state.get("missing_fields", [])
    answer = state.get("answer")
    
    # If there are missing fields and we have a clarification question, end to ask user
    if missing_fields and answer:
        return END
    else:
        # All required info collected, proceed to itinerary
        return "itinerary"

graph.add_conditional_edges("clarification", route_clarification)

# Small talk and itinerary both end
graph.add_edge("small_talk", END)
graph.add_edge("itinerary", END)

# Compile the graph
try:
    app = graph.compile()
    print("Trip planning graph compiled successfully with ChatGoogleGenerativeAI")
except Exception as e:
    print(f"Error compiling graph: {e}")
    raise

def process_message(user_message: str, previous_state: dict = None) -> dict:
    """
    Process a user message with optional previous state for API usage.
    
    Args:
        user_message: The current user message
        previous_state: Dictionary containing previous conversation state (optional)
    
    Returns:
        Dictionary containing updated state and response
    """
    try:
        # Create or update state
        if previous_state:
            # Convert dict to TripState and update with new message
            state = TripState(**previous_state)
            state["query"] = user_message
        else:
            # Create new state for first message
            state = TripState()
            state["query"] = user_message
            state["summary"] = ""
            state["history"] = []
            state["preferences"] = {}
            state["missing_fields"] = []
            state["itinerary_done"] = False
            state["trip_plan"] = None
        
        # Run the graph
        result = app.invoke(state)
        
        # Convert result to serializable dict for API response
        response_state = {
            "summary": result.get("summary", ""),
            "history": result.get("history", []),
            "query": result.get("query", ""),
            "intent": result.get("intent"),
            "preferences": result.get("preferences", {}),
            "missing_fields": result.get("missing_fields", []),
            "answer": result.get("answer"),
            "itinerary_done": result.get("itinerary_done", False),
            "final_output": result.get("final_output"),
            "trip_plan": result.get("trip_plan")
        }
        
        return {
            "success": True,
            "response": result.get("answer", "I'm processing your request..."),
            "state": response_state
        }
        
    except Exception as e:
        print(f"Error processing message: {str(e)}")
        return {
            "success": False,
            "response": "I encountered an error while processing your message. Please try again.",
            "state": previous_state or {},
            "error": str(e)
        }
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from .nodes.summary_node import summary_node
from .nodes.intent import intent_node
from .nodes.preference import preference_node
from .nodes.itinerary_node import itinerary_node
from .nodes.small_talk import small_talk_node
from .nodes.clarification import clarification_node
from .state import TripState

# Initialize Gemini LLM using langchain_google_genai
# Prefer explicit API key over ADC to avoid runtime credential issues
_API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
if not _API_KEY:
    raise RuntimeError("Missing Google API key. Set GOOGLE_API_KEY or GEMINI_API_KEY.")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7,
    google_api_key=_API_KEY,
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

# Add nodes with error handling (avoid names that collide with state keys)
NODE_SUMMARY = "node_summary"
NODE_INTENT = "node_intent"
NODE_SMALL_TALK = "node_small_talk"
NODE_PREFERENCES = "node_preferences"
NODE_CLARIFICATION = "node_clarification"
NODE_ITINERARY = "node_itinerary"

graph.add_node(NODE_SUMMARY, safe_node_wrapper(summary_node, NODE_SUMMARY))
graph.add_node(NODE_INTENT, safe_node_wrapper(intent_node, NODE_INTENT))
graph.add_node(NODE_SMALL_TALK, safe_node_wrapper(small_talk_node, NODE_SMALL_TALK))
graph.add_node(NODE_PREFERENCES, safe_node_wrapper(preference_node, NODE_PREFERENCES))
graph.add_node(NODE_CLARIFICATION, safe_node_wrapper(clarification_node, NODE_CLARIFICATION))
graph.add_node(NODE_ITINERARY, safe_node_wrapper(itinerary_node, NODE_ITINERARY))

# Set entry point
graph.set_entry_point(NODE_SUMMARY)

# Edges
graph.add_edge(NODE_SUMMARY, NODE_INTENT)

# Route based on intent with fallback
def route_intent(state: TripState):
    intent = state.get("intent", "").lower()
    if intent == "small_talk":
        return NODE_SMALL_TALK
    elif intent in ["trip_planning"]:
        return NODE_PREFERENCES
    else:
        # Default to preferences for ambiguous cases
        return NODE_PREFERENCES

graph.add_conditional_edges(NODE_INTENT, route_intent)

# Preferences → Clarification
graph.add_edge(NODE_PREFERENCES, NODE_CLARIFICATION)

# Clarification → either end (to ask user) or go to itinerary
def route_clarification(state: TripState):
    missing_fields = state.get("missing_fields", [])
    answer = state.get("answer")
    
    # If there are missing fields and we have a clarification question, end to ask user
    if missing_fields and answer:
        return END
    else:
        # All required info collected, proceed to itinerary
        return NODE_ITINERARY

graph.add_conditional_edges(NODE_CLARIFICATION, route_clarification)

# Small talk and itinerary both end
graph.add_edge(NODE_SMALL_TALK, END)
graph.add_edge(NODE_ITINERARY, END)

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

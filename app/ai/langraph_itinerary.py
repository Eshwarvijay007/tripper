from __future__ import annotations
from langgraph.graph import StateGraph, END
from app.ai.itinerary_nodes.state import PlanState
from app.ai.itinerary_nodes.entry import intent
from app.ai.itinerary_nodes.intent import node_parse_intent
from app.ai.itinerary_nodes.validate import node_check_missing
from app.ai.itinerary_nodes.trip_validation import node_validate_trip_requirements
from app.ai.itinerary_nodes.enrich import node_enrich
from app.ai.itinerary_nodes.pois import node_retrieve_pois
from app.ai.itinerary_nodes.plan import node_plan_days
from app.ai.itinerary_nodes.hotels import node_search_hotels
from app.ai.itinerary_nodes.finalize import node_finalize
from app.ai.itinerary_nodes.small_talk import node_small_talk


def build_graph() -> StateGraph:
    sg = StateGraph(PlanState)

    # location (lattitude longitude)  
    # accomodation room type
    # kitne din ka stay hai
    # budget
    # travel mode

    #type of user mode - family, couple, solo, friends
    # special needs - accessibility, dietary, pet friendly
    # trip type - adventure, leisure, business, wellness, cultural, romantic, family, solo



    #small talk agent node
    # if intent is not small talk, then check with the user details if we require more information
    # if more information is required, then ask the user for more information




    sg.add_node("entry_point", intent)
    sg.add_node("small_talk", node_small_talk)
    sg.add_node("parse_intent", node_parse_intent)
    sg.add_node("check_missing", node_check_missing)
    sg.add_node("validate_trip", node_validate_trip_requirements)
    sg.add_node("enrich", node_enrich)
    sg.add_node("retrieve_pois", node_retrieve_pois)
    sg.add_node("plan_days", node_plan_days)
    sg.add_node("search_hotels", node_search_hotels)
    sg.add_node("finalize", node_finalize)

    sg.set_entry_point("entry_point")
    sg.add_conditional_edges("entry_point", lambda x: x.get("next"), {
        "parse_intent": "parse_intent",
        "small_talk_response": "small_talk",
        "unknown_response": "small_talk"  # Handle unknown as small talk for now
    })
    sg.add_conditional_edges("parse_intent", lambda x: x.get("next"), {"validate_trip": "validate_trip"})
    sg.add_conditional_edges(
        "validate_trip",
        lambda x: x.get("next"),
        {"enrich": "enrich", "finalize": "finalize"},
    )
    sg.add_conditional_edges(
        "check_missing",
        lambda x: x.get("next"),
        {"enrich": "enrich", "finalize": "finalize"},
    )
    sg.add_conditional_edges("enrich", lambda x: x.get("next"), {"retrieve_pois": "retrieve_pois"})
    sg.add_conditional_edges("retrieve_pois", lambda x: x.get("next"), {"plan_days": "plan_days"})
    sg.add_conditional_edges(
        "plan_days", lambda x: x.get("next"), {"search_hotels": "search_hotels", "finalize": "finalize"}
    )
    sg.add_conditional_edges(
        "search_hotels", lambda x: x.get("next"), {"finalize": "finalize"}
    )
    sg.add_edge("finalize", END)
    sg.add_edge("small_talk", END)
    return sg

from __future__ import annotations
from langgraph.graph import StateGraph, END
from app.ai.itinerary_nodes.state import PlanState
from app.ai.itinerary_nodes.entry import node_entry_point
from app.ai.itinerary_nodes.intent import node_parse_intent
from app.ai.itinerary_nodes.validate import node_check_missing
from app.ai.itinerary_nodes.enrich import node_enrich
from app.ai.itinerary_nodes.pois import node_retrieve_pois
from app.ai.itinerary_nodes.plan import node_plan_days
from app.ai.itinerary_nodes.hotels import node_search_hotels
from app.ai.itinerary_nodes.finalize import node_finalize


def build_graph() -> StateGraph:
    sg = StateGraph(PlanState)
    sg.add_node("entry_point", node_entry_point)
    sg.add_node("parse_intent", node_parse_intent)
    sg.add_node("check_missing", node_check_missing)
    sg.add_node("enrich", node_enrich)
    sg.add_node("retrieve_pois", node_retrieve_pois)
    sg.add_node("plan_days", node_plan_days)
    sg.add_node("search_hotels", node_search_hotels)
    sg.add_node("finalize", node_finalize)

    sg.set_entry_point("entry_point")
    sg.add_conditional_edges("entry_point", lambda x: x.get("next"), {"parse_intent": "parse_intent"})
    sg.add_conditional_edges("parse_intent", lambda x: x.get("next"), {"check_missing": "check_missing"})
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
    return sg

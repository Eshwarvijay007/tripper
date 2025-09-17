from __future__ import annotations
from typing import Any, Dict, List, Optional

from fastapi import APIRouter

from app.ai.langraph_itinerary import build_graph
from app.schemas.itinerary import Itinerary, TravelerInfo, ItineraryConstraints, DayPlan, Activity
from app.schemas.common import Location
from app.ai.memory import build_context, populate_state_from_memory


router = APIRouter(prefix="/api/agent", tags=["agent"])


def _normalize_location_dict(d: Optional[dict]) -> Optional[dict]:
    if not d:
        return None
    # Ensure only expected Location fields are present
    allowed = {"city", "country", "lat", "lon", "iata", "dest_id", "dest_type"}
    return {k: d.get(k) for k in allowed if k in d}


@router.post("/plan")
def agent_plan(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Runs the itinerary planning agent.

    Request shape (flexible):
    {
      "user_text": str | null,
      "user_id": str | null,  # Optional user identifier for memory
      "state": { optional partial PlanState keys }
    }

    Response:
      - If more info needed: { need_info: true, questions: [str], state: {...} }
      - Else itinerary: { need_info: false, itinerary: {...} }
    """
    user_text: Optional[str] = payload.get("user_text")
    user_id: Optional[str] = payload.get("user_id", "anonymous")  # Default to anonymous
    state_in: Dict[str, Any] = payload.get("state") or {}

    # Build initial state for graph (dict-based)
    init_state: Dict[str, Any] = {}
    if user_text:
        init_state["user_text"] = str(user_text)
        init_state["user_id"] = user_id
        
        # Build memory context if user_text is provided
        try:
            memory_context = build_context(user_id, user_text)
            # Use the formatted context which includes recent conversation and preferences
            formatted_context = memory_context.get("formatted_context", "")
            init_state["short_term_memory"] = formatted_context
        except Exception as e:
            # Don't fail if memory system has issues
            print(f"Memory context failed: {e}")
            init_state["short_term_memory"] = ""

    # Allow passing partial state across turns
    for k in (
        "origin",
        "destinations",
        "date_range",
        "nights",
        "interests",
        "pace",
        "with_kids",
        "must_do",
        "avoid",
        "currency",
        "budget",
    ):
        if k in state_in and state_in.get(k) is not None:
            init_state[k] = state_in.get(k)
    
    # Populate state with user preferences from memory (only if not already present)
    try:
        original_state = dict(init_state)
        init_state = populate_state_from_memory(user_id, init_state)
        
        # Debug: Log what was populated from memory
        populated_fields = []
        for key, value in init_state.items():
            if key not in original_state and value:
                populated_fields.append(f"{key}: {value}")
        
        if populated_fields:
            print(f"Populated from memory for user {user_id}: {', '.join(populated_fields)}")
            
    except Exception as e:
        print(f"Failed to populate state from memory: {e}")
        # Continue without memory population

    # Normalize location structures if present
    if isinstance(init_state.get("origin"), dict):
        init_state["origin"] = _normalize_location_dict(init_state.get("origin"))
    if isinstance(init_state.get("destinations"), list):
        init_state["destinations"] = [
            _normalize_location_dict(d) for d in init_state["destinations"] if isinstance(d, dict)
        ]

    # Compile and run the local LangGraph itinerary planner
    graph = build_graph().compile()
    out: Dict[str, Any] = graph.invoke(init_state)  # type: ignore

    # If the planner surfaced an error (e.g., LLM failure), present it as a follow-up message
    if out.get("error"):
        msg = str(out.get("error"))
        return {
            "need_info": True,
            "questions": [msg],
            "state": {
                k: out.get(k)
                for k in (
                    "origin",
                    "destinations",
                    "date_range",
                    "nights",
                    "interests",
                    "pace",
                    "with_kids",
                    "must_do",
                    "avoid",
                    "currency",
                    "budget",
                )
                if out.get(k) is not None
            },
        }

    # If questions were identified, return them for a follow-up turn
    if out.get("need_info"):
        return {
            "need_info": True,
            "questions": out.get("questions", []),
            "state": {
                # Send back only whitelisted keys that help continue the turn
                k: out.get(k)
                for k in (
                    "origin",
                    "destinations",
                    "date_range",
                    "nights",
                    "interests",
                    "pace",
                    "with_kids",
                    "must_do",
                    "avoid",
                    "currency",
                    "budget",
                )
                if out.get(k) is not None
            },
        }

    # Otherwise, convert the planned state into an Itinerary-like payload
    dests = [Location(**d) for d in (out.get("destinations") or [])]
    day_plans_raw = out.get("day_plans") or []
    day_plans: List[DayPlan] = []
    for d in day_plans_raw:
        acts = [Activity(**a) if not isinstance(a, Activity) else a for a in (d.get("activities") or [])]
        dp = DayPlan(
            index=d.get("index", len(day_plans)),
            date=d.get("date"),
            summary=d.get("summary"),
            activities=acts,
            pinned=d.get("pinned", False),
        )
        day_plans.append(dp)

    iti = Itinerary(
        id="temp-agent-itinerary",
        trip_title="Your Trip",
        origin=(Location(**out["origin"]) if isinstance(out.get("origin"), dict) else None),
        destinations=dests,
        traveler=TravelerInfo(),
        constraints=ItineraryConstraints(),
        days=day_plans,
        offers=[],
        status="ready",
    )

    return {
        "need_info": False,
        "itinerary": iti.model_dump(),
        "hotel_options": out.get("hotel_options", []),
    }

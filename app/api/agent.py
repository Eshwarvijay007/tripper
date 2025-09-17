from __future__ import annotations
import uuid
from typing import Any, Dict, List, Optional

from fastapi import APIRouter

from app.ai.langraph_itinerary import build_graph
from app.schemas.itinerary import Itinerary, TravelerInfo, ItineraryConstraints, DayPlan, Activity
from app.schemas.common import Location
from app.services.conversation_repository import ensure_conversation, append_message


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
      "state": { optional partial PlanState keys }
    }

    Response:
      - If more info needed: { need_info: true, questions: [str], state: {...} }
      - Else itinerary: { need_info: false, itinerary: {...} }
    """
    conv_id: str = payload.get("conversation_id") or str(uuid.uuid4())
    ensure_conversation(conv_id)

    user_text: Optional[str] = payload.get("user_text")
    state_in: Dict[str, Any] = payload.get("state") or {}

    if user_text:
        append_message(
            conv_id,
            str(uuid.uuid4()),
            "user",
            user_text,
            extra={"source": "agent_plan"},
        )

    # Build initial state for graph (dict-based)
    init_state: Dict[str, Any] = {}
    if user_text:
        init_state["user_text"] = str(user_text)

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
    ):
        if k in state_in and state_in.get(k) is not None:
            init_state[k] = state_in.get(k)

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
        response = {
            "conversation_id": conv_id,
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
                )
                if out.get(k) is not None
            },
        }
        append_message(
            conv_id,
            str(uuid.uuid4()),
            "assistant",
            response["questions"],
            extra={"type": "agent_plan_error"},
        )
        return response

    # If questions were identified, return them for a follow-up turn
    if out.get("need_info"):
        response = {
            "conversation_id": conv_id,
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
                )
                if out.get(k) is not None
            },
        }
        append_message(
            conv_id,
            str(uuid.uuid4()),
            "assistant",
            response["questions"],
            extra={"type": "agent_plan_questions"},
        )
        return response

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

    response = {
        "conversation_id": conv_id,
        "need_info": False,
        "itinerary": iti.model_dump(),
        "hotel_options": out.get("hotel_options", []),
    }
    append_message(
        conv_id,
        str(uuid.uuid4()),
        "assistant",
        {
            "itinerary": response["itinerary"],
            "hotel_options": response["hotel_options"],
        },
        extra={"type": "agent_plan_itinerary"},
    )
    return response

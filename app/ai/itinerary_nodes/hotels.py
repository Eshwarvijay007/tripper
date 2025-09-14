from __future__ import annotations
from app.ai.tools import tool_search_hotels
from app.schemas.search import HotelSearchRequest
from app.schemas.common import DateRange, Location
from .state import PlanState


def node_search_hotels(state: PlanState) -> PlanState:
    dests = state.get("destinations") or []
    dr = state.get("date_range")
    if not dests or not isinstance(dr, dict) or not dr.get("start") or not dr.get("end"):
        state["hotel_options"] = []
        state["next"] = "finalize"
        return state
    # Build typed request; ensure valid dates
from pydantic import ValidationError

    try:
        dates = DateRange(**dr)  # type: ignore
    except ValidationError:
        state["hotel_options"] = []
        state["next"] = "finalize"
        return state
    h_req = HotelSearchRequest(
        destination=Location(**dests[0]),
        dates=dates,
        rooms=1,
        adults=2,
        children=0,
        currency=state.get("currency") or "USD",
    )
    res = tool_search_hotels(h_req)
    state["hotel_options"] = (res.get("options") or [])[:5]
    state["next"] = "finalize"
    return state

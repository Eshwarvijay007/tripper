from __future__ import annotations
from typing import List
from app.ai.tools import tool_search_poi
from app.schemas.search import PoiSearchRequest
from app.schemas.common import Location
from .state import PlanState


def node_retrieve_pois(state: PlanState) -> PlanState:
    poi_items: List[dict] = []
    dests = state.get("destinations") or []
    if dests:
        d0 = dests[0]
        if d0.get("lat") is not None and d0.get("lon") is not None:
            req = PoiSearchRequest(location=Location(**d0))
            poi_items = tool_search_poi(req).get("items", [])
    state["poi_candidates"] = poi_items
    state["next"] = "plan_days"
    return state


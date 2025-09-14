from __future__ import annotations
from typing import List
from app.services.geo import enrich_location
from app.schemas.common import Location
from .state import PlanState, _to_location


def node_enrich(state: PlanState) -> PlanState:
    raw_dests = state.get("destinations") or []
    dests: List[dict] = []
    for d in raw_dests:
        loc = _to_location(d)
        if loc is not None:
            dests.append(enrich_location(loc).model_dump())
    state["destinations"] = dests
    if (orig := state.get("origin")) is not None:
        oloc = _to_location(orig)
        if oloc is not None:
            state["origin"] = enrich_location(oloc).model_dump()
    state["next"] = "retrieve_pois"
    return state


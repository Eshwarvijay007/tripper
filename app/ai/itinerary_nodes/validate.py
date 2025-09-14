from __future__ import annotations
from typing import List
from .state import PlanState


def node_check_missing(state: PlanState) -> PlanState:
    qs: List[str] = []
    opts = state.get("disambiguate_options") or []
    if opts:
        name = (state.get("destinations") or [{}])[0].get("city") or "this place"
        labels = []
        for o in opts[:5]:
            city = o.get("city") or name
            country = o.get("country") or ""
            labels.append(f"{city}{(', ' + country) if country else ''}")
        qs.append(f"There are multiple places named '{name}'. Which one do you mean? " + ", ".join(labels) + ".")
        state["need_info"] = True
        state["questions"] = qs
        state["next"] = "finalize"
        return state

    dests = state.get("destinations") or []
    if not dests:
        qs.append("Where do you want to go?")
    dr = state.get("date_range")
    has_date_range = isinstance(dr, dict) and bool(dr.get("start")) and bool(dr.get("end"))
    nval = state.get("nights")
    try:
        nint = int(nval) if nval is not None else None
    except Exception:
        nint = None
    if nint is not None and (nint < 1 or nint > 365):
        nint = None
    if nint is None:
        state.pop("nights", None)
    has_nights = nint is not None
    if not has_date_range:
        if has_nights:
            qs.append("What dates do you plan to travel?")
        else:
            qs.append("What are your dates or how many nights (1-21)?")
    if qs:
        state["need_info"] = True
        state["questions"] = qs
        state["next"] = "finalize"
    else:
        state["need_info"] = False
        state["questions"] = []
        state["next"] = "enrich"
    return state

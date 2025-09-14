from __future__ import annotations
from .state import PlanState


def node_entry_point(state: PlanState) -> PlanState:
    state["next"] = "parse_intent"
    return state


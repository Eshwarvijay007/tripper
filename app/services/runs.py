from __future__ import annotations
import threading
from typing import Any, Dict, List

from app.ai.langraph_itinerary import build_graph
from langgraph.checkpoint.memory import MemorySaver
from app.schemas.itinerary import TripCreateRequest, Itinerary, DayPlan, Activity
from app.schemas.common import Location
from app.services.store import RUNS, RUN_EVENTS, ITINERARIES


def _push(run_id: str, name: str, **payload: Any) -> None:
    RUN_EVENTS.setdefault(run_id, []).append({"event": name, **payload})


def _worker(run_id: str, req: TripCreateRequest) -> None:
    try:
        RUNS[run_id] = {"id": run_id, "type": "itinerary", "status": "running"}
        events: List[Dict[str, Any]] = []
        _push(run_id, "run_started", run_id=run_id)
        # Build initial dict state for LangGraph (local execution)
        init_state: Dict[str, Any] = {
            "origin": req.origin.model_dump() if req.origin else None,
            "destinations": [d.model_dump() for d in (req.destinations or [])],
            "date_range": (req.constraints.date_range.model_dump() if (req.constraints and req.constraints.date_range) else None),
            "nights": (req.constraints.nights if req.constraints else None),
            "interests": (req.constraints.interests if req.constraints else []),
            "pace": (req.constraints.pace if req.constraints else None),
            "with_kids": False,
            "must_do": (req.constraints.must_do if req.constraints else []),
            "avoid": (req.constraints.avoid if req.constraints else []),
            "currency": (req.constraints.currency if req.constraints and req.constraints.currency else "INR"),
        }

        memory = MemorySaver()
        graph = build_graph().compile(checkpointer=memory)
        acc_state: Dict[str, Any] = {k: v for k, v in init_state.items() if v is not None}
        config = {"configurable": {"thread_id": run_id}}
        for update in graph.stream(init_state, config=config, stream_mode="updates"):
            for node_name, delta in update.items():
                if isinstance(delta, dict):
                    acc_state.update({k: v for k, v in delta.items() if v is not None})
                    changed = list(delta.keys())
                else:
                    changed = []
                _push(run_id, "node_completed", node=node_name, changed=changed)

        if acc_state.get("error"):
            msg = str(acc_state.get("error"))
            _push(run_id, "error", message=msg)
            RUNS[run_id] = {"id": run_id, "type": "itinerary", "status": "failed", "error": msg}
            return
        if acc_state.get("need_info"):
            qs = acc_state.get("questions") or []
            _push(run_id, "error", message=(qs[0] if qs else "Planner requires more information"))
            RUNS[run_id] = {"id": run_id, "type": "itinerary", "status": "failed", "error": (qs[0] if qs else "need_info")}
            return

        # Convert final state into Itinerary
        dests = [Location(**d) for d in (acc_state.get("destinations") or [])]
        day_plans_raw = acc_state.get("day_plans") or []
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

        itinerary = Itinerary(
            id=str(__import__("uuid").uuid4()),
            trip_title=req.title or "Your Trip",
            origin=(Location(**acc_state["origin"]) if isinstance(acc_state.get("origin"), dict) else None),
            destinations=dests,
            traveler=req.traveler,
            constraints=req.constraints,
            days=day_plans,
            offers=[],
            status="ready",
        )

        # Persist itinerary
        ITINERARIES[itinerary.id] = itinerary.model_dump()

        _push(run_id, "final", itinerary_id=itinerary.id)
        RUNS[run_id]["status"] = "completed"
    except Exception as e:  # pragma: no cover
        RUNS[run_id] = {"id": run_id, "type": "itinerary", "status": "failed", "error": str(e)}
        _push(run_id, "error", message=str(e))


def start_run_itinerary(req: TripCreateRequest) -> Dict[str, Any]:
    import uuid

    run_id = str(uuid.uuid4())
    # Initialize empty event list for SSE consumers to start listening immediately
    RUN_EVENTS[run_id] = []
    # Start worker thread
    t = threading.Thread(target=_worker, args=(run_id, req), daemon=True)
    t.start()
    RUNS[run_id] = {"id": run_id, "type": "itinerary", "status": "running"}
    return {"id": run_id, "status": RUNS[run_id]["status"]}

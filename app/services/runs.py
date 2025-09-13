from __future__ import annotations
import threading
from typing import Any, Dict, List

from app.ai.state import GraphState
from app.ai.graph import PlannerRunner
from app.schemas.itinerary import TripCreateRequest, Itinerary
from app.services.store import RUNS, RUN_EVENTS, ITINERARIES


def _push(run_id: str, name: str, **payload: Any) -> None:
    RUN_EVENTS.setdefault(run_id, []).append({"event": name, **payload})


def _worker(run_id: str, req: TripCreateRequest) -> None:
    try:
        RUNS[run_id] = {"id": run_id, "type": "itinerary", "status": "running"}
        events: List[Dict[str, Any]] = []
        _push(run_id, "run_started", run_id=run_id)

        # Initialize planning state
        state = GraphState(
            run_id=run_id,
            origin=req.origin,
            destinations=req.destinations or [],
            date_range=(req.constraints.date_range if req.constraints else None),
            nights=(req.constraints.nights if req.constraints else None),
            interests=(req.constraints.interests if req.constraints else []),
            pace=(req.constraints.pace if req.constraints else None),
            must_do=(req.constraints.must_do if req.constraints else []),
            avoid=(req.constraints.avoid if req.constraints else []),
            budget=(req.constraints.budget if req.constraints else None),
            currency=(req.constraints.currency if req.constraints else "USD"),
        )

        runner = PlannerRunner()
        itinerary: Itinerary = runner.run(state, events)

        # Backfill required fields from request (traveler, constraints, title)
        itinerary.trip_title = req.title or itinerary.trip_title or "Your Trip"
        itinerary.traveler = req.traveler
        itinerary.constraints = req.constraints

        # Persist itinerary
        ITINERARIES[itinerary.id] = itinerary.model_dump()

        # Flush node events to RUN_EVENTS
        for evt in events:
            _push(run_id, evt.get("event", "event"), **{k: v for k, v in evt.items() if k != "event"})

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


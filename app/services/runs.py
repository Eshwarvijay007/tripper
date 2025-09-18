from __future__ import annotations
import threading
from typing import Any, Dict, List

from app.schemas.itinerary import TripCreateRequest
from app.services.store import RUNS, RUN_EVENTS


def _push(run_id: str, name: str, **payload: Any) -> None:
    RUN_EVENTS.setdefault(run_id, []).append({"event": name, **payload})


def _worker(run_id: str, req: TripCreateRequest) -> None:
    # Graph execution has been removed; immediately mark as failed with a clear message.
    RUNS[run_id] = {"id": run_id, "type": "itinerary", "status": "failed", "error": "Itinerary graph removed"}
    _push(run_id, "run_started", run_id=run_id)
    _push(run_id, "error", message="Itinerary graph removed")
    _push(run_id, "final", itinerary_id=None)


def start_run_itinerary(req: TripCreateRequest) -> Dict[str, Any]:
    import uuid

    run_id = str(uuid.uuid4())
    # Initialize event list and immediately fail (no background graph)
    RUN_EVENTS[run_id] = []
    _worker(run_id, req)
    return {"id": run_id, "status": RUNS[run_id]["status"], "error": RUNS[run_id].get("error")}

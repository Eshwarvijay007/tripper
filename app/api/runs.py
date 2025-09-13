from __future__ import annotations
import uuid
from typing import Iterator
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from ..schemas.itinerary import TripCreateRequest
from ..services.store import RUNS, RUN_EVENTS


router = APIRouter(prefix="/api/runs", tags=["runs"])


@router.post("/itinerary")
def start_itinerary_run(req: TripCreateRequest) -> dict:
    run_id = str(uuid.uuid4())
    # minimal run record
    RUNS[run_id] = {
        "id": run_id,
        "type": "itinerary",
        "status": "running",
    }
    # Seed a canned sequence of events for the stream
    RUN_EVENTS[run_id] = [
        {"event": "run_started", "run_id": run_id},
        {"event": "node_started", "node": "parse_intent"},
        {"event": "node_completed", "node": "parse_intent"},
        {"event": "node_started", "node": "retrieve_pois"},
        {"event": "tool_result", "tool": "poi_search", "items": 12},
        {"event": "partial_itinerary", "days": 1},
        {"event": "node_started", "node": "search_flights"},
        {"event": "tool_result", "tool": "flights", "options": 3},
        {"event": "offers_found", "count": 4},
        {"event": "final"},
    ]
    # Mark as completed for the stub
    RUNS[run_id]["status"] = "completed"
    return {"id": run_id, "status": RUNS[run_id]["status"]}


@router.get("/{run_id}")
def get_run(run_id: str) -> dict:
    run = RUNS.get(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return run


def _sse_lines(run_id: str) -> Iterator[bytes]:
    events = RUN_EVENTS.get(run_id, [])
    for evt in events:
        # format as Server-Sent Events
        if (name := evt.get("event")):
            yield f"event: {name}\n".encode()
        yield f"data: {evt}\n\n".encode()


@router.get("/{run_id}/stream")
def stream_run(run_id: str):
    if run_id not in RUNS:
        raise HTTPException(status_code=404, detail="Run not found")
    return StreamingResponse(_sse_lines(run_id), media_type="text/event-stream")


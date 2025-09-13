from __future__ import annotations
from typing import Iterator
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from ..schemas.itinerary import TripCreateRequest
from ..services.store import RUNS, RUN_EVENTS
from ..services.runs import start_run_itinerary as _start_run_itinerary


router = APIRouter(prefix="/api/runs", tags=["runs"])


@router.post("/itinerary")
def start_itinerary_run(req: TripCreateRequest) -> dict:
    return _start_run_itinerary(req)


@router.get("/{run_id}")
def get_run(run_id: str) -> dict:
    run = RUNS.get(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return run


def _sse_lines(run_id: str) -> Iterator[bytes]:
    # Yield current snapshot and any future events added while the client holds the connection.
    # For now, we only emit the current set; background worker appends as it runs.
    events = RUN_EVENTS.get(run_id, [])
    for evt in events:
        if (name := evt.get("event")):
            yield f"event: {name}\n".encode()
        yield f"data: {evt}\n\n".encode()


@router.get("/{run_id}/stream")
def stream_run(run_id: str):
    if run_id not in RUNS:
        raise HTTPException(status_code=404, detail="Run not found")
    return StreamingResponse(_sse_lines(run_id), media_type="text/event-stream")

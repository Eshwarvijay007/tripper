from __future__ import annotations
import uuid
from datetime import date
from typing import Optional
from fastapi import APIRouter, HTTPException, status

from ..schemas.itinerary import (
    TripCreateRequest,
    Itinerary,
    ItineraryUpdateRequest,
    DayPlan,
    Activity,
)
from ..schemas.jobs import JobStatus
from ..services.store import ITINERARIES, JOBS


router = APIRouter(prefix="/api/itineraries", tags=["itineraries"])


@router.post("", response_model=JobStatus, status_code=status.HTTP_202_ACCEPTED)
def create_itinerary(req: TripCreateRequest):
    itinerary_id = str(uuid.uuid4())
    job_id = str(uuid.uuid4())

    # Create a stub itinerary immediately to let clients fetch it
    days = []
    total_days = req.constraints.nights or 3
    for i in range(total_days):
        days.append({
            "index": i,
            "date": None,
            "summary": f"Day {i+1} highlights in destination",
            "activities": [
                {
                    "id": str(uuid.uuid4()),
                    "name": "Sample attraction",
                    "category": "sight",
                    "location": req.destinations[0] if req.destinations else None,
                    "start_time": None,
                    "end_time": None,
                    "cost": None,
                    "notes": "This is a placeholder activity",
                    "source": "stub",
                }
            ],
        })

    itinerary = Itinerary(
        id=itinerary_id,
        trip_title=req.title or "Your Trip",
        origin=req.origin,
        destinations=req.destinations,
        traveler=req.traveler,
        constraints=req.constraints,
        days=days,  # type: ignore
        offers=[],
        status="ready",
    )
    ITINERARIES[itinerary_id] = itinerary.model_dump()

    JOBS[job_id] = {
        "id": job_id,
        "status": "completed",
        "result_type": "itinerary",
        "result_id": itinerary_id,
    }

    return JobStatus(**JOBS[job_id])


@router.get("/{itinerary_id}", response_model=Itinerary)
def get_itinerary(itinerary_id: str):
    it = ITINERARIES.get(itinerary_id)
    if not it:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    return it


@router.patch("/{itinerary_id}", response_model=Itinerary)
def update_itinerary(itinerary_id: str, req: ItineraryUpdateRequest):
    it = ITINERARIES.get(itinerary_id)
    if not it:
        raise HTTPException(status_code=404, detail="Itinerary not found")

    if req.title:
        it["trip_title"] = req.title
    if req.constraints:
        # shallow merge for scaffold
        it["constraints"].update(req.constraints.model_dump(exclude_unset=True))
    # ignore activity mutations for scaffold; mark status ready
    it["status"] = "ready"
    ITINERARIES[itinerary_id] = it
    return it


@router.post("/{itinerary_id}/regenerate", response_model=JobStatus, status_code=status.HTTP_202_ACCEPTED)
def regenerate_itinerary(itinerary_id: str):
    it = ITINERARIES.get(itinerary_id)
    if not it:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    job_id = str(uuid.uuid4())
    JOBS[job_id] = {
        "id": job_id,
        "status": "completed",
        "result_type": "itinerary",
        "result_id": itinerary_id,
    }
    return JobStatus(**JOBS[job_id])


@router.patch("/{itinerary_id}/constraints", response_model=Itinerary)
def update_constraints(itinerary_id: str, constraints: dict):
    it = ITINERARIES.get(itinerary_id)
    if not it:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    # deep-ish merge for scaffold
    it["constraints"] = {**it.get("constraints", {}), **constraints}
    ITINERARIES[itinerary_id] = it
    return it


@router.post("/{itinerary_id}/days/{day_index}/pin", response_model=Itinerary)
def pin_day(itinerary_id: str, day_index: int):
    it = ITINERARIES.get(itinerary_id)
    if not it:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    days = it.get("days", [])
    if day_index < 0 or day_index >= len(days):
        raise HTTPException(status_code=400, detail="Invalid day index")
    days[day_index]["pinned"] = True
    ITINERARIES[itinerary_id] = it
    return it


@router.post("/{itinerary_id}/days/{day_index}/unpin", response_model=Itinerary)
def unpin_day(itinerary_id: str, day_index: int):
    it = ITINERARIES.get(itinerary_id)
    if not it:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    days = it.get("days", [])
    if day_index < 0 or day_index >= len(days):
        raise HTTPException(status_code=400, detail="Invalid day index")
    days[day_index]["pinned"] = False
    ITINERARIES[itinerary_id] = it
    return it


@router.post("/{itinerary_id}/days/{day_index}/activities:add", response_model=Itinerary)
def add_activity(itinerary_id: str, day_index: int, activity: Activity):
    it = ITINERARIES.get(itinerary_id)
    if not it:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    days = it.get("days", [])
    if day_index < 0 or day_index >= len(days):
        raise HTTPException(status_code=400, detail="Invalid day index")
    days[day_index].setdefault("activities", []).append(activity.model_dump())
    ITINERARIES[itinerary_id] = it
    return it


@router.delete("/{itinerary_id}/days/{day_index}/activities/{activity_id}", response_model=Itinerary)
def remove_activity(itinerary_id: str, day_index: int, activity_id: str):
    it = ITINERARIES.get(itinerary_id)
    if not it:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    days = it.get("days", [])
    if day_index < 0 or day_index >= len(days):
        raise HTTPException(status_code=400, detail="Invalid day index")
    acts = days[day_index].get("activities", [])
    days[day_index]["activities"] = [a for a in acts if a.get("id") != activity_id]
    ITINERARIES[itinerary_id] = it
    return it


@router.post("/{itinerary_id}/days/{day_index}/activities:reorder", response_model=Itinerary)
def reorder_activities(itinerary_id: str, day_index: int, order: dict):
    it = ITINERARIES.get(itinerary_id)
    if not it:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    ids = order.get("order", [])
    days = it.get("days", [])
    if day_index < 0 or day_index >= len(days):
        raise HTTPException(status_code=400, detail="Invalid day index")
    by_id = {a.get("id"): a for a in days[day_index].get("activities", [])}
    days[day_index]["activities"] = [by_id[i] for i in ids if i in by_id]
    ITINERARIES[itinerary_id] = it
    return it


@router.get("/{itinerary_id}/summary")
def itinerary_summary(itinerary_id: str):
    it = ITINERARIES.get(itinerary_id)
    if not it:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    return {
        "id": it["id"],
        "trip_title": it.get("trip_title"),
        "days": len(it.get("days", [])),
        "destinations": [d.get("city") or d.get("country") for d in it.get("destinations", []) if d],
    }


@router.post("/{itinerary_id}/publish")
def publish_itinerary(itinerary_id: str):
    it = ITINERARIES.get(itinerary_id)
    if not it:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    # naive slug
    title = (it.get("trip_title") or "trip").lower().replace(" ", "-")
    slug = f"{title}/{itinerary_id[:12]}"
    it["public_slug"] = slug
    ITINERARIES[itinerary_id] = it
    return {"public_slug": slug}


@router.post("/{itinerary_id}/export/pdf", response_model=JobStatus, status_code=status.HTTP_202_ACCEPTED)
def export_pdf(itinerary_id: str):
    it = ITINERARIES.get(itinerary_id)
    if not it:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    job_id = str(uuid.uuid4())
    from ..services.store import JOBS
    JOBS[job_id] = {
        "id": job_id,
        "status": "completed",
        "result_type": "pdf",
        "result_id": itinerary_id,
    }
    return JobStatus(**JOBS[job_id])

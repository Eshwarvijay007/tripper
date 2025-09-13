from __future__ import annotations
from fastapi import APIRouter, HTTPException, Query

from ..providers.booking_rapidapi import search_destination, search_flight_destinations


router = APIRouter(prefix="/api/booking", tags=["booking"])


@router.get("/destinations")
def booking_destinations(query: str = Query(..., min_length=2), locale: str | None = None):
    try:
        items = search_destination(query, locale)
        return {"items": items}
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Booking destinations failed: {e}")


@router.get("/flight-destinations")
def booking_flight_destinations(query: str = Query(..., min_length=2), locale: str | None = None):
    try:
        items = search_flight_destinations(query, locale)
        return {"items": items}
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Booking flight destinations failed: {e}")

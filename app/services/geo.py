from __future__ import annotations
from typing import Optional

from app.schemas.common import Location
from app.providers import booking_rapidapi as booking


def _pick_city_like(items: list[dict]) -> Optional[dict]:
    for it in items:
        dt = (it.get("dest_type") or "").lower()
        did = str(it.get("dest_id", ""))
        if dt in ("city", "region", "district") or did.startswith("-"):
            return it
    return items[0] if items else None


def enrich_location(loc: Location, *, locale: str = "en-us") -> Location:
    """Ensure a Location has lat/lon (and dest_id/dest_type when possible).

    Uses Booking.com RapidAPI searchDestination to resolve city-like inputs.
    """
    if (loc.lat is not None and loc.lon is not None) and (loc.dest_id is not None and loc.dest_type is not None):
        return loc
    if not (loc.city or loc.country):
        return loc
    query = loc.city or loc.country or ""
    try:
        items = booking.search_destination(query, locale=locale)
        pick = _pick_city_like(items)
        if not pick:
            return loc
        # Build an enriched copy
        return Location(
            city=loc.city or pick.get("city_name"),
            country=loc.country or pick.get("country"),
            lat=loc.lat if loc.lat is not None else pick.get("lat"),
            lon=loc.lon if loc.lon is not None else pick.get("lon"),
            iata=loc.iata,
            dest_id=loc.dest_id or (str(pick.get("dest_id")) if pick.get("dest_id") is not None else None),
            dest_type=loc.dest_type or (str(pick.get("dest_type")) if pick.get("dest_type") is not None else None),
        )
    except Exception:
        # Best-effort enrichment; return original on failure
        return loc


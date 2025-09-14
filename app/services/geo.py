from __future__ import annotations
from typing import Optional, List, Dict, Any

from app.schemas.common import Location
from app.providers import booking_rapidapi as booking
from app.providers import google_places
from haversine import haversine, Unit
import logging

logger = logging.getLogger(__name__)

def _pick_city_like(items: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    for it in items:
        dt = (it.get("dest_type") or "").lower()
        did = str(it.get("dest_id", ""))
        if dt in ("city", "region", "district") or did.startswith("-"):
            return it
    return items[0] if items else None


def _closest_booking_to(lat: float, lon: float, items: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Pick booking destination closest to given lat/lon.

    Returns None if input list is empty or items lack coordinates.
    """
    if not items:
        return None
    ref = (lat, lon)
    best = None
    best_km = None
    for it in items:
        blat = it.get("lat")
        blon = it.get("lon")
        if blat is None or blon is None:
            continue
        km = haversine(ref, (blat, blon), unit=Unit.KILOMETERS)
        if best_km is None or km < best_km:
            best = it
            best_km = km
    return best or items[0]


def enrich_location(loc: Location, *, locale: str = "en-us") -> Location:
    """Ensure a Location has lat/lon (and dest_id/dest_type when possible).

    Uses Booking.com RapidAPI searchDestination to resolve city-like inputs.
    """
    if (loc.lat is not None and loc.lon is not None) and (loc.dest_id is not None and loc.dest_type is not None):
        return loc
    if not (loc.city or loc.country):
        return loc
    query = loc.city or loc.country or ""
    place_lat = loc.lat
    place_lon = loc.lon
    place_city = loc.city
    place_country = loc.country

    # First, try Google Places to resolve ambiguity and get stable coordinates
    try:
        q = query if not place_country else f"{query}, {place_country}"
        pdata = google_places.text_search_v1(q, limit=3)
        pitems = pdata.get("items", [])
        if pitems:
            # Prefer locality-type; else first
            def _score(p: Dict[str, Any]) -> int:
                types = [t.lower() for t in (p.get("types") or [])]
                score = 0
                if "locality" in types:
                    score += 3
                if "administrative_area_level_3" in types or "administrative_area_level_2" in types:
                    score += 2
                name = (p.get("name") or "").strip().lower()
                if place_city and name == place_city.strip().lower():
                    score += 2
                country = (p.get("country") or "").strip().lower()
                if place_country and country and place_country.strip().lower() == country:
                    score += 1
                return score

            pitems_sorted = sorted(pitems, key=_score, reverse=True)
            bestp = pitems_sorted[0]
            place_lat = place_lat if place_lat is not None else bestp.get("lat")
            place_lon = place_lon if place_lon is not None else bestp.get("lon")
            place_city = place_city or bestp.get("city_name") or bestp.get("name")
            place_country = place_country or bestp.get("country")
    except Exception:
        # ignore Places failures; continue with Booking only
        pass

    # Next, use Booking destinations; if Places gave coords, choose closest booking match
    try:
        items = booking.search_destination(query, locale=locale)
        pick = None
        if place_lat is not None and place_lon is not None:
            pick = _closest_booking_to(place_lat, place_lon, items)
        if pick is None:
            pick = _pick_city_like(items)
        if not pick:
            return loc
        return Location(
            city=place_city or pick.get("city_name"),
            country=place_country or pick.get("country"),
            lat=place_lat if place_lat is not None else pick.get("lat"),
            lon=place_lon if place_lon is not None else pick.get("lon"),
            iata=loc.iata,
            dest_id=loc.dest_id or (str(pick.get("dest_id")) if pick.get("dest_id") is not None else None),
            dest_type=loc.dest_type or (str(pick.get("dest_type")) if pick.get("dest_type") is not None else None),
        )
    except Exception:
        return loc

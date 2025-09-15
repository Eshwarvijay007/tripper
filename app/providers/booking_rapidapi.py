from __future__ import annotations
import os
from typing import Any, Dict, List

import requests


def _config() -> tuple[str, str, str]:
    host = os.getenv("BOOKING_RAPIDAPI_HOST", "booking-com15.p.rapidapi.com")
    base = os.getenv("BOOKING_RAPIDAPI_BASE", f"https://{host}")
    key = os.getenv("BOOKING_RAPIDAPI_KEY", "")
    return host, base, key


def _headers() -> Dict[str, str]:
    host, _base, key = _config()
    if not key:
        raise RuntimeError("Missing BOOKING_RAPIDAPI_KEY env var")
    return {
        "x-rapidapi-host": host,
        "x-rapidapi-key": key,
        "Accept": "application/json",
    }


def search_destination(query: str, locale: str | None = None) -> List[Dict[str, Any]]:
    """Call RapidAPI Booking.com searchDestination endpoint to resolve destination suggestions.

    Returns a simplified list: [{ dest_id, dest_type, name, city_name, country, lat, lon, image_url }]
    """
    host, base, _key = _config()
    url = f"{base}/api/v1/hotels/searchDestination"
    params = {"query": query}
    if locale:
        params["locale"] = locale
    r = requests.get(url, headers=_headers(), params=params, timeout=10)
    r.raise_for_status()
    data = r.json() or {}
    items = data.get("data", []) or []
    out: List[Dict[str, Any]] = []
    for it in items:
        out.append({
            "dest_id": it.get("dest_id"),
            "dest_type": it.get("dest_type"),
            "name": it.get("name") or it.get("label"),
            "city_name": it.get("city_name"),
            "country": it.get("country"),
            "lat": it.get("latitude"),
            "lon": it.get("longitude"),
            "image_url": it.get("image_url"),
            "region": it.get("region"),
        })
    return out

def _pick_city_dest_id(items: List[Dict[str, Any]]) -> str | None:
    # Prefer city/region-like entries; Booking city UFIs are often negative
    for it in items:
        dt = (it.get("dest_type") or "").lower()
        did = str(it.get("dest_id", ""))
        if dt in ("city", "region", "district") or (did.startswith("-")):
            return did
    return str(items[0].get("dest_id")) if items else None


def search_hotels_by_city(
    *,
    city: str,
    arrival_date: str,
    departure_date: str,
    adults: int = 2,
    children_qty: int = 0,
    children_age: str | None = None,
    room_qty: int = 1,
    page_number: int = 1,
    languagecode: str = "en-us",
    currency_code: str = "INR",
    units: str = "metric",
    temperature_unit: str = "c",
) -> Dict[str, Any]:
    # Resolve dest_id for the city first
    items = search_destination(city, locale=languagecode)
    dest_id = _pick_city_dest_id(items)
    if not dest_id:
        raise RuntimeError(f"No destination found for city='{city}'")
    return search_hotels_by_dest(
        dest_id=dest_id,
        search_type="CITY",
        arrival_date=arrival_date,
        departure_date=departure_date,
        adults=adults,
        children_qty=children_qty,
        children_age=children_age,
        room_qty=room_qty,
        page_number=page_number,
        languagecode=languagecode,
        currency_code=currency_code,
        location=city,
        units=units,
        temperature_unit=temperature_unit,
    )


def search_hotels_by_dest(
    *,
    dest_id: str,
    search_type: str = "CITY",
    arrival_date: str,
    departure_date: str,
    adults: int = 2,
    children_qty: int = 0,
    children_age: str | None = None,
    room_qty: int = 1,
    page_number: int = 1,
    languagecode: str = "en-us",
    currency_code: str = "INR",
    location: str | None = None,
    units: str = "metric",
    temperature_unit: str = "c",
) -> Dict[str, Any]:
    host, base, _key = _config()
    url = f"{base}/api/v1/hotels/searchHotels"
    params: Dict[str, Any] = {
        "dest_id": dest_id,
        "search_type": search_type,
        "arrival_date": arrival_date,
        "departure_date": departure_date,
        "adults": adults,
        "room_qty": room_qty,
        "page_number": page_number,
        "units": units,
        "temperature_unit": temperature_unit,
        "languagecode": languagecode,
        "currency_code": currency_code,
    }
    if location:
        params["location"] = location
    if children_qty and children_qty > 0:
        # RapidAPI expects a comma-separated ages string, e.g., "0,17"
        params["children_qty"] = children_qty
        params["children_age"] = children_age or ",".join(["8"] * children_qty)
    r = requests.get(url, headers=_headers(), params=params, timeout=12)
    r.raise_for_status()
    return r.json() or {}


def search_flight_destinations(query: str, locale: str | None = None) -> List[Dict[str, Any]]:
    """Call RapidAPI Booking.com flights searchDestination endpoint for airport/city codes.

    Returns a simplified list: [{ code, type, name, cityCode, cityName, regionName, country, photoUri, distanceKm }]
    """
    host, base, _key = _config()
    url = f"{base}/api/v1/flights/searchDestination"
    params: Dict[str, Any] = {"query": query}
    if locale:
        params["locale"] = locale
    r = requests.get(url, headers=_headers(), params=params, timeout=10)
    r.raise_for_status()
    data = r.json() or {}
    items = data.get("data", []) or []
    out: List[Dict[str, Any]] = []
    for it in items:
        dist = (it.get("distanceToCity") or {}).get("value")
        out.append({
            "code": it.get("code"),
            "type": it.get("type"),
            "name": it.get("name"),
            "cityCode": it.get("city"),
            "cityName": it.get("cityName"),
            "regionName": it.get("regionName"),
            "country": it.get("countryName") or it.get("country"),
            "photoUri": it.get("photoUri"),
            "distanceKm": dist,
        })
    return out

from __future__ import annotations
import os
from typing import Any, Dict, List, Optional

import requests


def _api_key() -> str:
    key = os.getenv("GOOGLE_PLACES_API_KEY") or os.getenv("GOOGLE_MAPS_API_KEY")
    if not key:
        raise RuntimeError("Missing GOOGLE_PLACES_API_KEY (or GOOGLE_MAPS_API_KEY)")
    return key


def nearby_attractions(
    *, lat: float, lon: float, radius: int = 5000, language: str | None = None
) -> Dict[str, Any]:
    """Call Google Places Nearby Search for tourist attractions near lat/lon.

    Returns dict with items: [{ name, place_id, lat, lon, rating, user_ratings, photo_url }]
    """
    key = _api_key()
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params: Dict[str, Any] = {
        "key": key,
        "location": f"{lat},{lon}",
        "radius": radius,
        "type": "tourist_attraction",
    }
    if language:
        params["language"] = language
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    data = r.json() or {}
    results = data.get("results", []) or []
    items: List[Dict[str, Any]] = []
    for res in results:
        geom = (res.get("geometry") or {}).get("location") or {}
        lat2 = geom.get("lat")
        lon2 = geom.get("lng")
        photos = res.get("photos") or []
        photo_ref = photos[0].get("photo_reference") if photos else None
        photo_url = (
            f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference={photo_ref}&key={key}"
            if photo_ref
            else None
        )
        items.append(
            {
                "name": res.get("name"),
                "place_id": res.get("place_id"),
                "lat": lat2,
                "lon": lon2,
                "rating": res.get("rating"),
                "user_ratings": res.get("user_ratings_total"),
                "photo": photo_url,
                "open_now": ((res.get("opening_hours") or {}).get("open_now")),
            }
        )
    return {"items": items}


def text_search(query: str, *, language: str | None = None, region: str | None = None) -> Dict[str, Any]:
    """Google Places Text Search to resolve places (cities, regions, POIs) from free text.

    Returns dict with items: [{ name, place_id, formatted_address, lat, lon, types[], photo, city_name, country }]
    """
    key = _api_key()
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params: Dict[str, Any] = {
        "key": key,
        "query": query,
    }
    if language:
        params["language"] = language
    if region:
        # ccTLD region bias, e.g., 'in', 'us'
        params["region"] = region.lower()
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    data = r.json() or {}
    status = (data.get("status") or "").upper()
    if status not in ("OK", "ZERO_RESULTS"):
        # Surface API errors to caller for easier debugging
        msg = data.get("error_message") or status
        raise RuntimeError(msg)
    results = data.get("results", []) or []
    items: List[Dict[str, Any]] = []
    for res in results:
        geom = (res.get("geometry") or {}).get("location") or {}
        lat = geom.get("lat")
        lon = geom.get("lng")
        types = res.get("types") or []
        photos = res.get("photos") or []
        photo_ref = photos[0].get("photo_reference") if photos else None
        photo_url = (
            f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference={photo_ref}&key={key}"
            if photo_ref
            else None
        )
        # Try to extract city and country from formatted address
        formatted = res.get("formatted_address") or ""
        parts = [p.strip() for p in formatted.split(",") if p.strip()]
        city_name = parts[-3] if len(parts) >= 3 else (parts[0] if parts else None)
        country = parts[-1] if parts else None

        items.append(
            {
                "place_id": res.get("place_id"),
                "name": res.get("name"),
                "formatted_address": formatted,
                "lat": lat,
                "lon": lon,
                "types": types,
                "photo": photo_url,
                "photo_ref": photo_ref,
                "city_name": city_name,
                "country": country,
            }
        )
    return {"items": items}


def text_search_v1(
    query: str,
    *,
    language: Optional[str] = None,
    region: Optional[str] = None,
    limit: Optional[int] = None,
) -> Dict[str, Any]:
    """Google Places API v1 Text Search.

    POST https://places.googleapis.com/v1/places:searchText
    Requires headers: X-Goog-Api-Key and X-Goog-FieldMask
    """
    key = _api_key()
    url = "https://places.googleapis.com/v1/places:searchText"

    body: Dict[str, Any] = {"textQuery": query}
    if language:
        body["languageCode"] = language
    if region:
        # ISO 3166-1 alpha-2 country code
        body["regionCode"] = region.upper()
    if limit:
        body["pageSize"] = limit

    field_mask = ",".join(
        [
            "places.id",
            "places.displayName",
            "places.formattedAddress",
            "places.location",
            "places.types",
            "places.photos",
        ]
    )

    headers = {
        "X-Goog-Api-Key": key,
        "X-Goog-FieldMask": field_mask,
        "Content-Type": "application/json",
    }

    r = requests.post(url, headers=headers, json=body, timeout=12)
    r.raise_for_status()
    data = r.json() or {}
    places = data.get("places", []) or []

    items: List[Dict[str, Any]] = []
    for pl in places:
        name_obj = pl.get("displayName") or {}
        display_name = name_obj.get("text") or pl.get("name")
        loc = (pl.get("location") or {})
        lat = loc.get("latitude")
        lon = loc.get("longitude")
        types = pl.get("types") or []
        photos = pl.get("photos") or []
        photo_url: Optional[str] = None
        if photos:
            photo_name = photos[0].get("name")  # e.g., "places/XXX/photos/YYY"
            if photo_name:
                # Construct media URL
                photo_url = f"https://places.googleapis.com/v1/{photo_name}/media?maxHeightPx=400&key={key}"

        formatted = pl.get("formattedAddress")

        # Try to infer city from address parts (best-effort)
        city_name: Optional[str] = None
        country: Optional[str] = None
        if isinstance(formatted, str) and formatted:
            parts = [p.strip() for p in formatted.split(",") if p.strip()]
            city_name = parts[-3] if len(parts) >= 3 else (parts[0] if parts else None)
            country = parts[-1] if parts else None

        items.append(
            {
                "place_id": pl.get("id") or pl.get("name"),
                "name": display_name,
                "formatted_address": formatted,
                "lat": lat,
                "lon": lon,
                "types": types,
                "photo": photo_url,
                "city_name": city_name or display_name,
                "country": country,
            }
        )

    return {"items": items}


# --- Lodging / Hotels (Places API v1) ---

def lodging_text_search_v1(location_name: str, *, limit: int = 10, language: Optional[str] = None) -> Dict[str, Any]:
    """Find lodging in a given location using Places API v1 Text Search.

    Returns: { items: [ { id, name, lat, lon } ] }
    """
    key = _api_key()
    url = "https://places.googleapis.com/v1/places:searchText"
    body: Dict[str, Any] = {
        "textQuery": f"lodging in {location_name}",
        "pageSize": min(max(limit, 1), 20),
    }
    if language:
        body["languageCode"] = language

    field_mask = ",".join([
        "places.id",
        "places.displayName",
        "places.location",
        "places.rating",
        "places.priceLevel",
        "places.photos",
        "places.formattedAddress",
    ])
    headers = {
        "X-Goog-Api-Key": key,
        "X-Goog-FieldMask": field_mask,
        "Content-Type": "application/json",
    }
    r = requests.post(url, headers=headers, json=body, timeout=12)
    r.raise_for_status()
    data = r.json() or {}
    places = data.get("places", []) or []
    items: List[Dict[str, Any]] = []
    for pl in places:
        name_obj = pl.get("displayName") or {}
        display_name = name_obj.get("text") or pl.get("name")
        loc = (pl.get("location") or {})
        lat = loc.get("latitude")
        lon = loc.get("longitude")
        photos = pl.get("photos") or []
        photo_url: Optional[str] = None
        if photos:
            photo_name = photos[0].get("name")
            if photo_name:
                photo_url = f"https://places.googleapis.com/v1/{photo_name}/media?maxHeightPx=800&key={key}"
        items.append({
            "id": pl.get("id") or pl.get("name"),
            "name": display_name,
            "lat": lat,
            "lon": lon,
            "rating": pl.get("rating"),
            "price_level": pl.get("priceLevel"),
            "photo": photo_url,
            "formatted_address": pl.get("formattedAddress"),
        })
    return {"items": items}


def place_details_v1(place_id: str) -> Dict[str, Any]:
    """Fetch details for a place, including editorial summary, photos, price level, rating.

    Returns the raw Places API v1 JSON.
    """
    key = _api_key()
    url = f"https://places.googleapis.com/v1/{place_id}"
    field_mask = ",".join([
        "editorialSummary",
        "photos",
        "priceLevel",
        "rating",
        "displayName",
        "formattedAddress",
        "location",
    ])
    headers = {
        "X-Goog-Api-Key": key,
        "X-Goog-FieldMask": field_mask,
        "Content-Type": "application/json",
    }
    r = requests.get(url, headers=headers, timeout=10)
    r.raise_for_status()
    data = r.json() or {}
    return data

from __future__ import annotations
import os
from typing import Any, Dict, List

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


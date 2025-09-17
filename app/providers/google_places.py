from __future__ import annotations
import os
from typing import Any, Dict, List, Optional, Tuple

import requests


def _api_key() -> str:
    key = os.getenv("GOOGLE_PLACES_API_KEY") or os.getenv("GOOGLE_MAPS_API_KEY")
    if not key:
        raise RuntimeError("Missing GOOGLE_PLACES_API_KEY (or GOOGLE_MAPS_API_KEY)")
    return key


def geocode(query: str, *, language: Optional[str] = None, region: Optional[str] = None) -> Dict[str, Any]:
    """Geocode a free-text query into lat/lon using Places API v1 Text Search.

    Returns: { items: [ { name, lat, lon, place_id, formatted_address } ] }
    """
    # Prefer v1 to avoid legacy errors
    data = text_search_v1(query, language=language, region=region)
    items = [
        {
            "name": it.get("name"),
            "lat": it.get("lat"),
            "lon": it.get("lon"),
            "place_id": it.get("place_id"),
            "formatted_address": it.get("formatted_address"),
        }
        for it in data.get("items", [])
        if it.get("lat") is not None and it.get("lon") is not None
    ]
    return {"items": items}


def nearby_search(
    *,
    lat: float,
    lon: float,
    radius: int = 5000,
    type_filter: Optional[str] = None,
    keyword: Optional[str] = None,
    language: Optional[str] = None,
) -> Dict[str, Any]:
    """Generalized Google Places Nearby Search helper.

    Returns dict with items: [{ name, place_id, lat, lon, rating, user_ratings, photo, types }]
    """
    key = _api_key()
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params: Dict[str, Any] = {
        "key": key,
        "location": f"{lat},{lon}",
        "radius": radius,
    }
    if type_filter:
        params["type"] = type_filter
    if keyword:
        params["keyword"] = keyword
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
                "types": res.get("types") or [],
                "formatted_address": res.get("vicinity"),
            }
        )
    return {"items": items}


def nearby_search_v1(
    *,
    lat: float,
    lon: float,
    radius: int = 5000,
    included_type: Optional[str] = None,
    keyword: Optional[str] = None,
    language: Optional[str] = None,
) -> Dict[str, Any]:
    """Places API v1 Nearby Search.

    POST https://places.googleapis.com/v1/places:searchNearby
    NOTE: keyword parameter is ignored in v1 API, use included_type instead
    """
    key = _api_key()
    url = "https://places.googleapis.com/v1/places:searchNearby"

    body: Dict[str, Any] = {
        "locationRestriction": {
            "circle": {
                "center": {"latitude": lat, "longitude": lon},
                "radius": float(radius),
            }
        },
        "pageSize": 20,
    }
    if language:
        body["languageCode"] = language
    if included_type:
        body["includedTypes"] = [included_type]
    # Note: keyword is not supported in Places API v1 searchNearby

    field_mask = ",".join(
        [
            "places.id",
            "places.displayName",
            "places.location",
            "places.rating",
            "places.userRatingCount",
            "places.types",
            "places.photos",
            "places.formattedAddress",
            "places.editorialSummary",
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
        lat2 = loc.get("latitude")
        lon2 = loc.get("longitude")
        photos = pl.get("photos") or []
        photo_url: Optional[str] = None
        if photos:
            photo_name = photos[0].get("name")
            if photo_name:
                photo_url = f"https://places.googleapis.com/v1/{photo_name}/media?maxHeightPx=400&key={key}"
        
        # Extract editorial summary for description
        editorial_summary = pl.get("editorialSummary", {})
        description = None
        if editorial_summary:
            description = editorial_summary.get("text")
        
        items.append(
            {
                "name": display_name,
                "place_id": pl.get("id") or pl.get("name"),
                "lat": lat2,
                "lon": lon2,
                "rating": pl.get("rating"),
                "user_ratings": pl.get("userRatingCount"),
                "photo": photo_url,
                "types": pl.get("types") or [],
                "formatted_address": pl.get("formattedAddress"),
                "description": description,
            }
        )
    return {"items": items}


def distance_matrix(
    origins: List[Tuple[float, float]],
    destinations: List[Tuple[float, float]],
) -> Dict[str, Any]:
    """Call Google Distance Matrix API (v1) to compute distances in meters and durations in seconds.

    Returns: { rows: [ { elements: [ { distance_meters, duration_seconds, status } ] } ] }
    """
    if not origins or not destinations:
        return {"rows": []}
    key = _api_key()
    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    origin_str = "|".join([f"{lat},{lon}" for lat, lon in origins])
    dest_str = "|".join([f"{lat},{lon}" for lat, lon in destinations])
    params = {
        "key": key,
        "origins": origin_str,
        "destinations": dest_str,
        "units": "metric",
    }
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    data = r.json() or {}
    rows = []
    for row in data.get("rows", []) or []:
        elements = []
        for el in row.get("elements", []) or []:
            distance_meters = ((el.get("distance") or {}).get("value"))
            duration_seconds = ((el.get("duration") or {}).get("value"))
            elements.append(
                {
                    "status": el.get("status"),
                    "distance_meters": distance_meters,
                    "duration_seconds": duration_seconds,
                }
            )
        rows.append({"elements": elements})
    return {"rows": rows}

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
            "places.editorialSummary",
            "places.rating",
            "places.userRatingCount",
            "places.internationalPhoneNumber",
            "places.nationalPhoneNumber",
            "places.websiteUri",
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

        # Extract editorial summary for description
        editorial_summary = pl.get("editorialSummary", {})
        description = None
        if editorial_summary:
            description = editorial_summary.get("text")
        
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
                "description": description,
                "rating": pl.get("rating"),
                "user_ratings": pl.get("userRatingCount"),
                "phone_number": pl.get("internationalPhoneNumber") or pl.get("nationalPhoneNumber"),
                "website": pl.get("websiteUri"),
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
        "places.internationalPhoneNumber",
        "places.nationalPhoneNumber",
        "places.websiteUri",
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
            "phone_number": pl.get("internationalPhoneNumber") or pl.get("nationalPhoneNumber"),
            "website": pl.get("websiteUri"),
        })
    return {"items": items}


def place_details_v1(place_id: str) -> Dict[str, Any]:
    """Fetch comprehensive details for a place.

    Returns processed place details with description, types, rating, etc.
    """
    key = _api_key()
    url = f"https://places.googleapis.com/v1/{place_id}"
    field_mask = ",".join([
        "editorialSummary",
        "generativeSummary",
        "photos",
        "priceLevel",
        "rating",
        "userRatingCount",
        "displayName",
        "formattedAddress",
        "location",
        "types",
        "primaryType",
        "shortFormattedAddress",
        "internationalPhoneNumber",
        "websiteUri",
        "businessStatus",
    ])
    headers = {
        "X-Goog-Api-Key": key,
        "X-Goog-FieldMask": field_mask,
        "Content-Type": "application/json",
    }
    r = requests.get(url, headers=headers, timeout=10)
    r.raise_for_status()
    data = r.json() or {}
    
    # Extract the best available description
    description = None
    
    # Try generative summary first (newer, more comprehensive)
    if data.get("generativeSummary"):
        description = data["generativeSummary"].get("text")
    
    # Fallback to editorial summary
    if not description and data.get("editorialSummary"):
        description = data["editorialSummary"].get("text")
    
    # Extract other useful information
    name_obj = data.get("displayName", {})
    display_name = name_obj.get("text") if name_obj else None
    
    return {
        "place_id": place_id,
        "name": display_name,
        "description": description,
        "rating": data.get("rating"),
        "user_rating_count": data.get("userRatingCount"),
        "types": data.get("types", []),
        "primary_type": data.get("primaryType"),
        "formatted_address": data.get("formattedAddress"),
        "raw_data": data  # Keep raw data for additional processing if needed
    }

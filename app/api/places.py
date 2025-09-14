from __future__ import annotations
from fastapi import APIRouter, HTTPException, Query

from ..providers import google_places


router = APIRouter(prefix="/api/places", tags=["places"])


@router.get("/suggest")
def places_suggest(
    query: str = Query(..., min_length=2),
    language: str | None = None,
    country: str | None = Query(None, description="2-letter country code (region bias), e.g., IN, US"),
    limit: int | None = Query(None, ge=1, le=50),
):
    try:
        # Prefer Places API v1 Text Search
        data = google_places.text_search_v1(
            query,
            language=language,
            region=(country.upper() if country else None),
            limit=limit,
        )
        items = []
        for it in data.get("items", []):
            # Normalize shape roughly similar to booking destinations for front-end reuse
            types = [t.lower() for t in (it.get("types") or [])]
            dest_type = "city" if any(t in types for t in ("locality", "administrative_area_level_3", "administrative_area_level_2")) else None
            items.append(
                {
                    "place_id": it.get("place_id"),
                    "dest_type": dest_type,  # optional
                    "name": it.get("name"),
                    "city_name": it.get("city_name") or it.get("name"),
                    "country": it.get("country"),
                    "lat": it.get("lat"),
                    "lon": it.get("lon"),
                    "image_url": it.get("photo"),
                    "formatted_address": it.get("formatted_address"),
                }
            )
        if limit is not None:
            items = items[:limit]
        return {"items": items}
    except Exception as e:
        # Fallback to legacy Text Search if v1 fails for any reason
        try:
            data2 = google_places.text_search(query, language=language, region=(country.lower() if country else None))
            items = []
            for it in data2.get("items", []):
                types = [t.lower() for t in (it.get("types") or [])]
                dest_type = "city" if any(t in types for t in ("locality", "administrative_area_level_3", "administrative_area_level_2")) else None
                items.append(
                    {
                        "place_id": it.get("place_id"),
                        "dest_type": dest_type,
                        "name": it.get("name"),
                        "city_name": it.get("city_name") or it.get("name"),
                        "country": it.get("country"),
                        "lat": it.get("lat"),
                        "lon": it.get("lon"),
                        "image_url": it.get("photo"),
                        "formatted_address": it.get("formatted_address"),
                    }
                )
            if limit is not None:
                items = items[:limit]
            return {"items": items}
        except Exception as e2:
            raise HTTPException(status_code=502, detail=f"Google Places suggest failed: {e} | fallback: {e2}")

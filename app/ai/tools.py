from __future__ import annotations
from typing import Any, Dict, List

from app.schemas.search import HotelSearchRequest, FlightSearchRequest, PoiSearchRequest
from app.schemas.common import Money, Currency
from app.providers import booking_rapidapi as booking
from app.providers import google_places


def tool_search_hotels(req: HotelSearchRequest) -> Dict[str, Any]:
    """Search hotels/lodging.

    Replaced with Google Places (v1) lodging search for richer details. Falls back to
    Booking RapidAPI only if Places key is missing.
    Returns dict: { options: [HotelOption-like dict], paging }
    """
    city = req.destination.city if req.destination else None
    currency = req.currency

    def _approx_price(price_level: str | None) -> float:
        levels = {
            "PRICE_LEVEL_FREE": 0.0,
            "PRICE_LEVEL_INEXPENSIVE": 75.0,
            "PRICE_LEVEL_MODERATE": 150.0,
            "PRICE_LEVEL_EXPENSIVE": 300.0,
            "PRICE_LEVEL_VERY_EXPENSIVE": 600.0,
        }
        return levels.get(str(price_level or "").upper(), 0.0)

    # Prefer Google Places v1 if key available
    try:
        # Quick check for API key; raises if missing
        _ = google_places._api_key()  # type: ignore
        if not city:
            return {"options": [], "paging": req.paging.model_dump()}
        search = google_places.lodging_text_search_v1(city, limit=10)
        items = search.get("items", [])
        options: List[Dict[str, Any]] = []
        for pl in items[:10]:
            place_id = pl.get("id") or pl.get("place_id")
            name = pl.get("name") or "Hotel"
            rating = pl.get("rating")
            price_level = pl.get("price_level")
            photo = pl.get("photo")
            # Fetch details for summary and potentially better photo
            try:
                details = google_places.place_details_v1(place_id) if place_id else {}
            except Exception:
                details = {}
            editorial = ((details.get("editorialSummary") or {}).get("text")) if isinstance(details, dict) else None
            if not photo:
                # try to extract from details
                photos = (details or {}).get("photos") or []
                if photos:
                    photo_name = photos[0].get("name")
                    key = google_places._api_key()  # type: ignore
                    if photo_name:
                        photo = f"https://places.googleapis.com/v1/{photo_name}/media?maxHeightPx=800&key={key}"
            amount = _approx_price(price_level)
            options.append(
                {
                    "id": str(place_id or name),
                    "name": name,
                    "stars": float(rating) if rating else None,
                    "neighborhood": pl.get("formatted_address"),
                    "price_per_night": Money(amount=round(amount, 2), currency=Currency(currency)).model_dump(),
                    "deeplink": None,
                    **({"photo": photo} if photo else {}),
                    **({"description": editorial} if editorial else {}),
                }
            )
        return {"options": options, "paging": req.paging.model_dump()}
    except Exception:
        # Fallback to Booking RapidAPI if configured
        pass

    # Fallback: Booking.com RapidAPI
    dest_id = req.destination.dest_id if req.destination else None
    dest_type = (req.destination.dest_type or "").upper() if req.destination else None
    nights = (req.dates.end - req.dates.start).days if req.dates else 1
    try:
        if dest_id:
            stype = dest_type or ("CITY" if str(dest_id).startswith("-") else "HOTEL")
            raw = booking.search_hotels_by_dest(
                dest_id=str(dest_id),
                search_type=stype,
                arrival_date=req.dates.start.isoformat() if req.dates else None,
                departure_date=req.dates.end.isoformat() if req.dates else None,
                adults=req.adults,
                children_qty=req.children or 0,
                room_qty=req.rooms,
                languagecode="en-us",
                currency_code=currency,
                location=city,
            )
        elif city:
            raw = booking.search_hotels_by_city(
                city=city,
                arrival_date=req.dates.start.isoformat() if req.dates else None,
                departure_date=req.dates.end.isoformat() if req.dates else None,
                adults=req.adults,
                children_qty=req.children or 0,
                room_qty=req.rooms,
                languagecode="en-us",
                currency_code=currency,
            )
        else:
            return {"options": [], "paging": req.paging.model_dump()}
    except Exception as e:
        return {"options": [], "paging": req.paging.model_dump(), "error": str(e)}

    data = (raw or {}).get("data", {})
    hotels = data.get("hotels", []) or []
    options: List[Dict[str, Any]] = []
    for h in hotels:
        p = h.get("property", {})
        price = ((p.get("priceBreakdown", {}) or {}).get("grossPrice", {}) or {})
        amount = float(price.get("value") or 0.0)
        per_night = amount / nights if nights and nights > 0 else amount
        stars = p.get("accuratePropertyClass") or p.get("propertyClass") or p.get("qualityClass") or 0
        photos = p.get("photoUrls") or []
        options.append(
            {
                "id": str(p.get("id")),
                "name": p.get("name") or "Hotel",
                "stars": float(stars) if stars else None,
                "neighborhood": p.get("wishlistName") or None,
                "price_per_night": Money(amount=round(per_night, 2), currency=Currency(currency)).model_dump(),
                "deeplink": None,
                **({"photo": photos[0]} if photos else {}),
            }
        )
    return {"options": options, "paging": req.paging.model_dump()}


def tool_search_flights(req: FlightSearchRequest) -> Dict[str, Any]:
    """Placeholder flight search; swap to real provider later."""
    from uuid import uuid4
    option = {
        "id": str(uuid4()),
        "carrier": "Sample Air",
        "depart_at": f"{req.dates.start}T08:00:00",
        "arrive_at": f"{req.dates.start}T12:10:00",
        "duration_minutes": 250,
        "price": Money(amount=199.0, currency=Currency(req.currency)).model_dump(),
        "deeplink": "https://partner.example/booking/flight/ABC",
    }
    return {"options": [option]}


def tool_search_poi(req: PoiSearchRequest) -> Dict[str, Any]:
    if req.location and req.location.lat is not None and req.location.lon is not None:
        try:
            data = google_places.nearby_attractions(lat=req.location.lat, lon=req.location.lon)
            items: List[Dict[str, Any]] = []
            for it in data.get("items", []):
                items.append(
                    {
                        "id": it.get("place_id"),
                        "name": it.get("name"),
                        "category": "attraction",
                        "lat": it.get("lat"),
                        "lon": it.get("lon"),
                        "score": it.get("rating"),
                        "photo": it.get("photo"),
                        "user_ratings": it.get("user_ratings"),
                        "open_now": it.get("open_now"),
                    }
                )
            return {"items": items, "paging": req.paging.model_dump()}
        except Exception as e:
            return {"items": [], "paging": req.paging.model_dump(), "error": str(e)}
    # No coords provided
    return {"items": [], "paging": req.paging.model_dump()}

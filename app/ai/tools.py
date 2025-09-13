from __future__ import annotations
from typing import Any, Dict, List

from app.schemas.search import HotelSearchRequest, FlightSearchRequest, PoiSearchRequest
from app.schemas.common import Money, Currency
from app.providers import booking_rapidapi as booking
from app.providers import google_places


def tool_search_hotels(req: HotelSearchRequest) -> Dict[str, Any]:
    """Thin wrapper around Booking RapidAPI search.

    Returns dict: { options: [HotelOption-like dict], paging: req.paging }
    """
    city = req.destination.city if req.destination else None
    dest_id = req.destination.dest_id if req.destination else None
    dest_type = (req.destination.dest_type or "").upper() if req.destination else None
    nights = (req.dates.end - req.dates.start).days
    try:
        if dest_id:
            stype = dest_type or ("CITY" if str(dest_id).startswith("-") else "HOTEL")
            raw = booking.search_hotels_by_dest(
                dest_id=str(dest_id),
                search_type=stype,
                arrival_date=req.dates.start.isoformat(),
                departure_date=req.dates.end.isoformat(),
                adults=req.adults,
                children_qty=req.children or 0,
                room_qty=req.rooms,
                languagecode="en-us",
                currency_code=req.currency,
                location=city,
            )
        elif city:
            raw = booking.search_hotels_by_city(
                city=city,
                arrival_date=req.dates.start.isoformat(),
                departure_date=req.dates.end.isoformat(),
                adults=req.adults,
                children_qty=req.children or 0,
                room_qty=req.rooms,
                languagecode="en-us",
                currency_code=req.currency,
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
        currency = price.get("currency") or req.currency
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


from __future__ import annotations
import uuid
from fastapi import APIRouter
from ..schemas.search import (
    FlightSearchRequest,
    FlightOption,
    HotelSearchRequest,
    HotelOption,
    PoiSearchRequest,
    Poi,
)
from ..schemas.common import Money, Currency
from ..providers import booking_rapidapi as booking
from ..providers import google_places


router = APIRouter(prefix="/api/search", tags=["search"])


@router.post("/flights")
def search_flights(req: FlightSearchRequest) -> dict:
    # Stubbed example flight options
    options = [
        FlightOption(
            id=str(uuid.uuid4()),
            carrier="Sample Air",
            depart_at=f"{req.dates.start}T08:00:00",
            arrive_at=f"{req.dates.start}T12:10:00",
            duration_minutes=250,
            price=Money(amount=199.0, currency=Currency(req.currency)),
            deeplink="https://partner.example/booking/flight/ABC",
        )
    ]
    return {"options": [o.model_dump() for o in options]}


@router.post("/hotels")
def search_hotels(req: HotelSearchRequest) -> dict:
    # Integrate Booking.com RapidAPI
    # Prefer explicit dest_id if provided; else resolve by city
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
            # Fallback not implemented: require city
            return {"options": [], "paging": req.paging.model_dump()}
    except Exception as e:
        return {"options": [], "paging": req.paging.model_dump(), "error": str(e)}

    data = (raw or {}).get("data", {})
    hotels = data.get("hotels", []) or []
    options = []
    for h in hotels:
        p = h.get("property", {})
        price = ((p.get("priceBreakdown", {}) or {}).get("grossPrice", {}) or {})
        currency = price.get("currency") or req.currency
        amount = float(price.get("value") or 0.0)
        per_night = amount / nights if nights and nights > 0 else amount
        stars = p.get("accuratePropertyClass") or p.get("propertyClass") or p.get("qualityClass") or 0
        photos = p.get("photoUrls") or []
        options.append(
            HotelOption(
                id=str(p.get("id")),
                name=p.get("name") or "Hotel",
                stars=float(stars) if stars else None,
                neighborhood=p.get("wishlistName") or None,
                price_per_night=Money(amount=round(per_night, 2), currency=Currency(currency)),
                deeplink=None,
            ).model_dump() | ({"photo": photos[0]} if photos else {})
        )
    return {"options": options, "paging": req.paging.model_dump()}


@router.post("/poi")
def search_poi(req: PoiSearchRequest) -> dict:
    # Use Google Places Nearby for attractions when lat/lon provided
    if req.location and req.location.lat is not None and req.location.lon is not None:
        try:
            data = google_places.nearby_attractions(
                lat=req.location.lat,
                lon=req.location.lon,
                # Google expects meters; sensible default radius ~5km
            )
            items = []
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
            return {"items": [], "error": str(e), "paging": req.paging.model_dump()}

    # Fallback stub
    pois = [
        Poi(
            id=str(uuid.uuid4()),
            name="Iconic Museum",
            category="museum",
            lat=req.location.lat if req.location else None,
            lon=req.location.lon if req.location else None,
            score=0.92,
        )
    ]
    return {"items": [p.model_dump() for p in pois], "paging": req.paging.model_dump()}

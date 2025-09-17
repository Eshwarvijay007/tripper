from __future__ import annotations

import math
import os
import time
from typing import Any, Dict, List, Optional, Tuple

from ..providers import google_places
from typing import Tuple


# --- Simple in-memory cache (process-local) ---
_CACHE: Dict[str, Tuple[float, Any]] = {}
_CACHE_TTL_SECONDS = int(os.getenv("TRIP_SUGGEST_CACHE_TTL", "900"))  # 15 minutes default


TRIP_TYPE_TO_QUERY: Dict[str, Dict[str, Any]] = {
    # These can be tuned further. We prefer keyword + type combos to bias results.
    "Adventure": {"keyword": "hiking OR trekking OR national park OR adventure", "type": None},
    "Leisure": {"keyword": "park OR promenade OR landmark OR attraction", "type": "tourist_attraction"},
    "Business": {"keyword": "convention center OR business district", "type": None},
    "Wellness": {"keyword": "spa OR wellness center OR hot spring", "type": None},
    "Cultural": {"keyword": "museum OR heritage site OR temple OR fort", "type": None},
    "Romantic": {"keyword": "romantic viewpoint OR sunset point OR beach", "type": None},
    "Family": {"keyword": "zoo OR theme park OR aquarium OR family attraction", "type": None},
    "Solo": {"keyword": "popular attraction OR museum OR walking tour", "type": None},
    "Friends/Group": {"keyword": "nightlife OR club OR market OR adventure park", "type": None},
    "Luxury": {"keyword": "luxury shopping OR fine dining OR art gallery", "type": None},
    "Budget/Backpacking": {"keyword": "backpacker hostel OR free attraction OR market", "type": None},
    "Eco/Nature": {"keyword": "nature reserve OR national park OR botanical garden", "type": None},
    "Spiritual/Pilgrimage": {"keyword": "temple OR church OR mosque OR monastery OR pilgrimage", "type": None},
    "Food & Wine": {"keyword": "famous restaurant OR street food OR food market OR winery", "type": "restaurant"},
    "Festival/Event": {"keyword": "festival venue OR event venue OR fairground", "type": None},
}

# Estimated visit durations in minutes based on place types and categories
VISIT_DURATION_MAP: Dict[str, int] = {
    # Museums and galleries - longer visits
    "museum": 120,
    "art_gallery": 90,
    "science_museum": 150,
    "history_museum": 120,
    
    # Religious and cultural sites
    "temple": 60,
    "church": 45,
    "mosque": 45,
    "monastery": 60,
    "shrine": 30,
    "heritage_site": 90,
    
    # Entertainment and attractions
    "amusement_park": 300,  # 5 hours
    "theme_park": 360,  # 6 hours
    "zoo": 180,  # 3 hours
    "aquarium": 120,
    "botanical_garden": 90,
    "park": 60,
    "tourist_attraction": 60,
    
    # Shopping and markets
    "shopping_mall": 120,
    "market": 90,
    "bazaar": 90,
    
    # Food and dining
    "restaurant": 90,
    "cafe": 45,
    "food_market": 60,
    
    # Nature and outdoor
    "national_park": 240,  # 4 hours
    "nature_reserve": 180,
    "beach": 120,
    "viewpoint": 30,
    "lighthouse": 45,
    
    # Architecture and landmarks
    "landmark": 45,
    "monument": 30,
    "castle": 120,
    "fort": 90,
    "palace": 120,
    
    # Default fallback
    "default": 60,
}


def _estimate_visit_duration(place_types: List[str], place_name: str = "") -> int:
    """Estimate visit duration in minutes based on place types and name."""
    if not place_types:
        return VISIT_DURATION_MAP["default"]
    
    # Check specific type matches first
    for place_type in place_types:
        place_type_lower = place_type.lower()
        if place_type_lower in VISIT_DURATION_MAP:
            return VISIT_DURATION_MAP[place_type_lower]
    
    # Check for partial matches in place name
    place_name_lower = place_name.lower()
    for keyword, duration in VISIT_DURATION_MAP.items():
        if keyword != "default" and keyword.replace("_", " ") in place_name_lower:
            return duration
    
    # Special handling for common patterns
    if any(t in ["tourist_attraction", "establishment", "point_of_interest"] for t in place_types):
        if "museum" in place_name_lower:
            return VISIT_DURATION_MAP["museum"]
        elif "temple" in place_name_lower or "shrine" in place_name_lower:
            return VISIT_DURATION_MAP["temple"]
        elif "market" in place_name_lower or "bazaar" in place_name_lower:
            return VISIT_DURATION_MAP["market"]
        elif "park" in place_name_lower:
            return VISIT_DURATION_MAP["park"]
    
    return VISIT_DURATION_MAP["default"]


# Currency conversion rates (approximate, for basic conversion)
# In production, use a real-time currency API like exchangerate-api.io
CURRENCY_TO_USD_RATES = {
    "USD": 1.0,
    "INR": 0.012,   # 1 INR ≈ 0.012 USD
    "EUR": 1.08,    # 1 EUR ≈ 1.08 USD
    "GBP": 1.27,    # 1 GBP ≈ 1.27 USD
    "CAD": 0.74,    # 1 CAD ≈ 0.74 USD
    "AUD": 0.66,    # 1 AUD ≈ 0.66 USD
    "JPY": 0.0067,  # 1 JPY ≈ 0.0067 USD
    "CNY": 0.14,    # 1 CNY ≈ 0.14 USD
    "THB": 0.029,   # 1 THB ≈ 0.029 USD
    "MYR": 0.22,    # 1 MYR ≈ 0.22 USD
    "SGD": 0.74,    # 1 SGD ≈ 0.74 USD
}

# Country to currency mapping
COUNTRY_TO_CURRENCY = {
    "india": "INR",
    "united states": "USD",
    "usa": "USD",
    "canada": "CAD",
    "united kingdom": "GBP",
    "uk": "GBP",
    "england": "GBP",
    "france": "EUR",
    "germany": "EUR",
    "spain": "EUR",
    "italy": "EUR",
    "netherlands": "EUR",
    "australia": "AUD",
    "japan": "JPY",
    "china": "CNY",
    "thailand": "THB",
    "malaysia": "MYR",
    "singapore": "SGD",
}


def _detect_currency_from_location(location: str, geo_data: Dict[str, Any] = None) -> str:
    """Detect likely currency based on location name or geocoded data."""
    location_lower = location.lower()
    
    # Try to extract country info from geocoded data
    if geo_data and geo_data.get("items"):
        first_result = geo_data["items"][0]
        country = (first_result.get("country") or "").lower()
        if country in COUNTRY_TO_CURRENCY:
            return COUNTRY_TO_CURRENCY[country]
    
    # Fallback: check location name for country hints
    for country, currency in COUNTRY_TO_CURRENCY.items():
        if country in location_lower:
            return currency
    
    # Default to USD if we can't determine
    return "USD"


def _convert_currency(amount: float, from_currency: str, to_currency: str = "USD") -> float:
    """Convert amount from one currency to another using approximate rates."""
    if from_currency == to_currency:
        return amount
    
    from_rate = CURRENCY_TO_USD_RATES.get(from_currency.upper(), 1.0)
    to_rate = CURRENCY_TO_USD_RATES.get(to_currency.upper(), 1.0)
    
    # Convert from_currency -> USD -> to_currency
    usd_amount = amount * from_rate
    final_amount = usd_amount / to_rate
    
    return round(final_amount, 2)


def _detect_budget_currency_and_convert(budget: Optional[float], location: str, geo_data: Dict[str, Any] = None) -> Tuple[Optional[float], str, str]:
    """Detect budget currency from location and convert to USD for internal processing.
    
    Returns:
        (budget_in_usd, original_currency, display_currency)
    """
    # Always detect currency from location, even if budget is None
    detected_currency = _detect_currency_from_location(location, geo_data)
    
    if budget is None or budget <= 0:
        return budget, detected_currency, detected_currency
    
    # Convert to USD for internal processing
    budget_usd = _convert_currency(budget, detected_currency, "USD")
    
    return budget_usd, detected_currency, detected_currency


def _format_duration(minutes: int) -> str:
    """Format duration from minutes to human-readable string."""
    if minutes < 60:
        return f"{minutes} min"
    else:
        hours = minutes // 60
        remaining_minutes = minutes % 60
        if remaining_minutes == 0:
            return f"{hours} hr" if hours == 1 else f"{hours} hrs"
        else:
            return f"{hours}h {remaining_minutes}m"


def _cache_get(key: str) -> Optional[Any]:
    item = _CACHE.get(key)
    if not item:
        return None
    ts, value = item
    if (time.time() - ts) > _CACHE_TTL_SECONDS:
        _CACHE.pop(key, None)
        return None
    return value


def _cache_set(key: str, value: Any) -> None:
    _CACHE[key] = (time.time(), value)


def _haversine_km(a: Tuple[float, float], b: Tuple[float, float]) -> float:
    R = 6371.0
    lat1, lon1 = math.radians(a[0]), math.radians(a[1])
    lat2, lon2 = math.radians(b[0]), math.radians(b[1])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    h = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )
    return 2 * R * math.asin(math.sqrt(h))


def _sequence_by_nearest_neighbor(points: List[Dict[str, Any]], start: Tuple[float, float]) -> List[Dict[str, Any]]:
    remaining = points[:]
    ordered: List[Dict[str, Any]] = []
    current = start
    while remaining:
        nearest_idx = min(
            range(len(remaining)),
            key=lambda i: _haversine_km(current, (remaining[i]["lat"], remaining[i]["lon"])),
        )
        next_point = remaining.pop(nearest_idx)
        ordered.append(next_point)
        current = (next_point["lat"], next_point["lon"])
    return ordered


def _chunk_days(items: List[Dict[str, Any]], no_of_days: int, per_day: int = 3) -> List[List[Dict[str, Any]]]:
    total = min(len(items), no_of_days * per_day)
    items = items[:total]
    days: List[List[Dict[str, Any]]] = []
    for i in range(0, total, per_day):
        days.append(items[i : i + per_day])
    return days


def get_stay_plan_suggestions(
    *,
    location: str,
    budget: Optional[float] = None,
    budget_currency: str = "USD",
    display_currency: str = "USD",
    language: Optional[str] = None,
    region: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Generate a list of accommodation options based on location and budget.
    
    Args:
        location: City or location name to search accommodations
        budget: Budget amount per night in USD (e.g., 2000 for $2000/night)
        language: Language code for responses
        region: Region code for search bias
    
    Returns:
        List of accommodation options with details
    """
    if not location:
        return []
    
    # Determine budget category from numeric budget
    budget_range = _determine_budget_category(budget)
    
    # Geocode location first
    geo_key = f"geocode::{location}::{language or ''}::{region or ''}"
    geo = _cache_get(geo_key)
    if not geo:
        geo = google_places.geocode(location, language=language, region=region)
        _cache_set(geo_key, geo)
    if not geo.get("items"):
        return []
    
    origin = geo["items"][0]
    origin_name = origin.get("name", location)
    
    # Define search queries based on budget category
    budget_queries = {
        "budget": ["budget hotels", "hostels", "guesthouses", "backpacker accommodation"],
        "mid-range": ["hotels", "boutique hotels", "bed and breakfast", "inns"],
        "luxury": ["luxury hotels", "5 star hotels", "resort", "premium accommodation"]
    }
    
    queries = budget_queries.get(budget_range.lower(), budget_queries["mid-range"])
    
    all_accommodations = []
    
    for query_term in queries:
        stay_key = f"stay::{origin_name}::{query_term}::{language or ''}::v1"
        stay_data = _cache_get(stay_key)
        
        if not stay_data:
            try:
                # Use text search for accommodations
                full_query = f"{query_term} in {origin_name}"
                stay_data = google_places.text_search_v1(
                    query=full_query,
                    language=language,
                    region=region,
                    limit=5
                )
            except Exception:
                # Fallback to lodging search
                try:
                    stay_data = google_places.lodging_text_search_v1(
                        origin_name, limit=5, language=language
                    )
                except Exception:
                    stay_data = {"items": []}
            _cache_set(stay_key, stay_data)
        
        # Process accommodations
        for item in stay_data.get("items", []):
            if item.get("name") and item.get("lat") and item.get("lon"):
                # Get enhanced details if place_id available
                place_id = item.get("place_id")
                enhanced_data = {}
                if place_id:
                    try:
                        enhanced_data = google_places.place_details_v1(place_id)
                    except Exception:
                        pass
                
                # Calculate price range based on price level and budget category
                price_level = item.get("price_level") or enhanced_data.get("raw_data", {}).get("priceLevel")
                pricing_info = _get_pricing_info(
                    price_level, budget_range, budget, budget_currency, display_currency
                )
                
                # Extract phone and website from enhanced_data
                raw_data = enhanced_data.get("raw_data", {})
                phone_number = (
                    raw_data.get("internationalPhoneNumber") or 
                    raw_data.get("nationalPhoneNumber") or 
                    item.get("phone_number")
                )
                website = (
                    raw_data.get("websiteUri") or 
                    raw_data.get("website") or 
                    item.get("website")
                )
                
                accommodation = {
                    "name": item.get("name"),
                    "location": origin_name,
                    "address": item.get("formatted_address", ""),
                    "rating": item.get("rating") or enhanced_data.get("rating"),
                    "pricing": pricing_info,
                    "links": {
                        "google_maps": f"https://maps.google.com/?q={item.get('lat')},{item.get('lon')}",
                        "website": website
                    },
                    "photos": [item.get("photo")] if item.get("photo") else [],
                    "coordinates": {
                        "lat": item.get("lat"),
                        "lng": item.get("lon")
                    },
                    "description": (
                        enhanced_data.get("description") or 
                        item.get("description") or 
                        f"Accommodation in {origin_name}"
                    ),
                    "category": _categorize_accommodation(item.get("name", ""), query_term),
                    "user_rating_count": (
                        item.get("user_ratings") or 
                        enhanced_data.get("user_rating_count")
                    ),
                    "phone": phone_number
                }
                
                # Avoid duplicates
                if not any(acc["name"] == accommodation["name"] for acc in all_accommodations):
                    all_accommodations.append(accommodation)
    
    # Filter and score accommodations based on budget if provided
    if budget is not None and budget > 0:
        budget_scored_accommodations = []
        
        for acc in all_accommodations:
            pricing = acc.get("pricing", {})
            range_min = pricing.get("range_min", 0)
            range_max = pricing.get("range_max", float('inf'))
            
            # Calculate budget relevance score (higher is better)
            budget_relevance_score = 0
            
            # Perfect match: budget falls within the accommodation's price range
            if range_min <= budget <= range_max:
                budget_relevance_score = 100
            # Good match: ranges overlap significantly
            elif (budget * 0.7 <= range_max and budget * 1.3 >= range_min):
                # Calculate overlap percentage
                overlap_start = max(range_min, budget * 0.7)
                overlap_end = min(range_max, budget * 1.3)
                overlap_size = max(0, overlap_end - overlap_start)
                range_size = max(1, range_max - range_min)
                overlap_ratio = overlap_size / range_size
                budget_relevance_score = int(50 + (overlap_ratio * 40))  # 50-90 score
            # Acceptable match: within reasonable distance
            elif abs(budget - (range_min + range_max) / 2) <= budget * 0.5:
                distance_ratio = abs(budget - (range_min + range_max) / 2) / budget
                budget_relevance_score = int(30 * (1 - distance_ratio))  # 0-30 score
            
            # Only include accommodations with some budget relevance
            if budget_relevance_score > 0:
                acc['budget_relevance_score'] = budget_relevance_score
                budget_scored_accommodations.append(acc)
        
        # Use scored list if we have results, otherwise fall back to all (but add low scores)
        if budget_scored_accommodations:
            all_accommodations = budget_scored_accommodations
        else:
            # Add minimal scores to all accommodations as fallback
            for acc in all_accommodations:
                acc['budget_relevance_score'] = 10
    
    # Sort by budget relevance (if available), then by rating, then by user rating count
    def sort_key(acc):
        budget_score = acc.get('budget_relevance_score', 0)
        rating = acc.get("rating") or 0
        user_ratings = acc.get("user_rating_count") or 0
        # Combine scores: budget relevance (40%), rating (40%), user ratings count (20%)
        combined_score = (budget_score * 0.4) + (rating * 20 * 0.4) + (min(user_ratings, 500) / 500 * 100 * 0.2)
        return combined_score
    
    all_accommodations.sort(key=sort_key, reverse=True)
    
    # Clean up internal scoring fields from final output
    for acc in all_accommodations:
        acc.pop('budget_relevance_score', None)
    
    # Return top 8 accommodations
    return all_accommodations[:8]


def _get_pricing_info(
    price_level: Optional[str], 
    budget_range: str, 
    user_budget: Optional[float] = None,
    user_budget_currency: str = "USD",
    display_currency: str = "USD"
) -> Dict[str, Any]:
    """Generate pricing information based on price level, budget category, and user's actual budget."""
    
    # Google Places API price level mapping to actual USD ranges
    google_price_ranges = {
        "PRICE_LEVEL_FREE": {"min": 0, "max": 15},
        "PRICE_LEVEL_INEXPENSIVE": {"min": 15, "max": 60},
        "PRICE_LEVEL_MODERATE": {"min": 60, "max": 150},
        "PRICE_LEVEL_EXPENSIVE": {"min": 150, "max": 400},
        "PRICE_LEVEL_VERY_EXPENSIVE": {"min": 400, "max": 1000}
    }
    
    # Budget category base ranges (more realistic thresholds)
    budget_category_ranges = {
        "budget": {"min": 10, "max": 60, "currency": "USD", "per": "night"},
        "mid-range": {"min": 60, "max": 250, "currency": "USD", "per": "night"},
        "luxury": {"min": 250, "max": 800, "currency": "USD", "per": "night"}
    }
    
    # Start with budget category as base
    base_range = budget_category_ranges.get(budget_range.lower(), budget_category_ranges["mid-range"])
    
    # If we have Google's price level, use it as primary source
    if price_level and str(price_level).upper() in google_price_ranges:
        google_range = google_price_ranges[str(price_level).upper()]
        price_min = google_range["min"]
        price_max = google_range["max"]
        level_display = price_level.replace("PRICE_LEVEL_", "").title()
    else:
        # When Google price level is not available, use user budget as primary guide
        if user_budget is not None and user_budget > 0:
            # Create a realistic range around user's budget (±30%)
            price_min = max(5, int(user_budget * 0.7))
            price_max = int(user_budget * 1.3)
            level_display = "Estimated"
        else:
            # Fallback to budget category range only when no user budget available
            price_min = base_range["min"]
            price_max = base_range["max"]
            level_display = budget_range.title()
    
    # If user provided a specific budget and we have Google price level, find the best intersection
    if user_budget is not None and user_budget > 0 and price_level and str(price_level).upper() in google_price_ranges:
        # Create a narrower range around user's budget (±25%)
        user_min = max(5, int(user_budget * 0.75))
        user_max = int(user_budget * 1.25)
        
        # Use the intersection of Google's price level and user's budget range
        final_min = max(price_min, user_min)
        final_max = min(price_max, user_max)
        
        # If the ranges don't overlap well, prefer user's budget but adjust slightly toward Google's range
        if final_min >= final_max:
            final_min = int(user_budget * 0.8)
            final_max = int(user_budget * 1.2)
            # Still respect Google's minimum if it's reasonable and not too far from user budget
            if price_min > 0 and final_max < price_min and price_min <= user_budget * 2:
                final_min = price_min
                final_max = int(price_min * 1.5)
    else:
        # Use the price range we calculated above (either from Google or user budget)
        final_min = price_min
        final_max = price_max
    
    # Convert final prices to display currency
    final_min_display = _convert_currency(max(5, final_min), "USD", display_currency)
    final_max_display = _convert_currency(final_max, "USD", display_currency)
    
    # Convert user budget to display currency for output
    user_budget_display = None
    if user_budget is not None:
        user_budget_display = _convert_currency(user_budget, "USD", display_currency)
    
    return {
        "range_min": int(final_min_display),
        "range_max": int(final_max_display), 
        "currency": display_currency,
        "per": "night",
        "level": level_display,
        "user_budget": int(user_budget_display) if user_budget_display else None,
        "user_budget_currency": user_budget_currency,
        "google_price_level": price_level
    }



def _determine_budget_category(budget: Optional[float]) -> str:
    """Determine budget category from numeric budget amount.
    
    Args:
        budget: Budget amount per night in USD
        
    Returns:
        Budget category: 'budget', 'mid-range', or 'luxury'
    """
    if budget is None:
        return "mid-range"
    
    # Updated budget thresholds (per night in USD) - more realistic
    if budget <= 60:
        return "budget"
    elif budget <= 250:
        return "mid-range"
    else:
        return "luxury"


def _categorize_accommodation(name: str, query_term: str) -> str:
    """Categorize accommodation type based on name and search term."""
    name_lower = name.lower()
    query_lower = query_term.lower()
    
    if "hostel" in name_lower or "backpack" in name_lower:
        return "Hostel"
    elif "resort" in name_lower:
        return "Resort"
    elif "boutique" in name_lower:
        return "Boutique Hotel"
    elif "inn" in name_lower or "b&b" in name_lower or "bed and breakfast" in name_lower:
        return "Inn/B&B"
    elif "guest" in name_lower:
        return "Guesthouse"
    elif "luxury" in query_lower or "5 star" in query_lower:
        return "Luxury Hotel"
    else:
        return "Hotel"


def get_trip_plan_suggestions(
    *,
    location: str,
    no_of_days_to_stay: int,
    trip_type: str,
    budget: Optional[float] = None,
    language: Optional[str] = None,
    region: Optional[str] = None,
    search_radius_m: int = 15000,
) -> Dict[str, Any]:
    """Generate a structured list of trip locations and stay options based on origin, days, trip type, and budget.

    Returns shape: { 
        trip_plan: [ { day: N, locations: [ { name, description, lat, lng, photo_url, distance_from_previous } ] } ],
        stay_plan: [ { name, location, address, rating, pricing, links, photos } ]
    }
    """
    if not location or not isinstance(no_of_days_to_stay, int) or no_of_days_to_stay <= 0:
        return {"trip_plan": [], "stay_plan": []}

    # Geocode origin
    geo_key = f"geocode::{location}::{language or ''}::{region or ''}"
    geo = _cache_get(geo_key)
    if not geo:
        geo = google_places.geocode(location, language=language, region=region)
        _cache_set(geo_key, geo)
    if not geo.get("items"):
        return {"trip_plan": [], "stay_plan": []}
    origin = geo["items"][0]
    origin_lat = float(origin["lat"])
    origin_lon = float(origin["lon"])
    
    # Detect currency and convert budget to USD for internal processing
    budget_usd, original_currency, display_currency = _detect_budget_currency_and_convert(
        budget, location, geo
    )

    # Trip-type-specific search strategy
    mapping = TRIP_TYPE_TO_QUERY.get(trip_type) or TRIP_TYPE_TO_QUERY.get("Leisure")
    keyword = mapping.get("keyword")
    type_filter = mapping.get("type")

    near_key = f"near::{origin_lat:.5f},{origin_lon:.5f}::{search_radius_m}::{keyword or ''}::{type_filter or ''}::{language or ''}::v2"
    near = _cache_get(near_key)
    if not near:
        # Strategy: Use text search for keyword-based queries, nearby search for type-based queries
        try:
            if keyword and not type_filter:
                # Use text search for keyword-based queries (more flexible)
                location_name = origin.get("name", "unknown location")
                query = f"{keyword.split(' OR ')[0]} near {location_name}"
                near = google_places.text_search_v1(
                    query=query,
                    language=language,
                    limit=20
                )
            else:
                # Use nearby search for type-based queries
                near = google_places.nearby_search_v1(
                    lat=origin_lat,
                    lon=origin_lon,
                    radius=search_radius_m,
                    included_type=type_filter,
                    language=language,
                )
        except Exception:
            # Fallback: legacy generalized nearby (best-effort), then attractions
            try:
                near = google_places.nearby_search(
                    lat=origin_lat,
                    lon=origin_lon,
                    radius=search_radius_m,
                    type_filter=type_filter,
                    keyword=keyword,
                    language=language,
                )
            except Exception:
                near = google_places.nearby_attractions(lat=origin_lat, lon=origin_lon, radius=search_radius_m, language=language)
        _cache_set(near_key, near)

    items = []
    for it in (near.get("items") or []):
        if it.get("lat") is not None and it.get("lon") is not None and it.get("name"):
            place_data = {
                "name": it.get("name"),
                "lat": float(it.get("lat")),
                "lon": float(it.get("lon")),
                "photo_url": it.get("photo"),
                "place_id": it.get("place_id") or it.get("id"),
                "description": it.get("description"),
                "types": it.get("types", []),
                "rating": it.get("rating"),
            }
            
            # Try to get better description from Place Details API
            if place_data["place_id"] and not place_data["description"]:
                try:
                    details = google_places.place_details_v1(place_data["place_id"])
                    if details and details.get("description"):
                        place_data["description"] = details["description"]
                        # Update types and rating if available
                        if details.get("types"):
                            place_data["types"] = details["types"]
                        if details.get("rating"):
                            place_data["rating"] = details["rating"]
                except Exception:
                    # Place details API call failed, continue with existing data
                    pass
            
            items.append(place_data)

    # Sequence by nearest-neighbor heuristic from origin
    ordered = _sequence_by_nearest_neighbor(items, (origin_lat, origin_lon))

    # Compute distances and travel durations between consecutive spots
    coords = [(o["lat"], o["lon"]) for o in ordered]
    distances_km: List[Optional[float]] = [None] * len(ordered)
    travel_durations_min: List[Optional[int]] = [None] * len(ordered)
    
    if len(coords) >= 2:
        distance_matrix_success = False
        try:
            # Google Distance Matrix API has limits - try in smaller batches if needed
            max_elements = 25  # Google allows up to 25 elements per request for free tier
            if len(coords) - 1 <= max_elements:
                dm = google_places.distance_matrix(coords[:-1], coords[1:])
                rows = dm.get("rows") or []
                if rows and len(rows) == len(coords) - 1:
                    for i, row in enumerate(rows):
                        el = (row.get("elements") or [{}])[0]
                        meters = el.get("distance_meters")
                        duration_seconds = el.get("duration_seconds")
                        status = el.get("status")
                        if status == "OK":
                            if isinstance(meters, (int, float)):
                                distances_km[i + 1] = round(meters / 1000.0, 1)
                                distance_matrix_success = True
                            if isinstance(duration_seconds, (int, float)):
                                travel_durations_min[i + 1] = round(duration_seconds / 60.0)
            else:
                # Too many coordinates, skip Distance Matrix API
                pass
        except Exception:
            # Distance Matrix API failed, will use fallback
            pass
        
        # Always fall back to haversine for distance if Distance Matrix didn't work
        if not distance_matrix_success:
            for i in range(1, len(coords)):
                dist = _haversine_km(coords[i - 1], coords[i])
                distances_km[i] = round(dist, 1)
                # Estimate travel duration based on distance (assume ~30 km/h average speed in cities)
                travel_durations_min[i] = max(5, round(dist * 2))  # Minimum 5 min, ~2 min per km
    
    # Ensure first item is 0 for distance and travel time
    if ordered:
        distances_km[0] = 0.0
        travel_durations_min[0] = 0

    per_day = 3 if no_of_days_to_stay <= 3 else 2  # lighter pace for longer trips
    day_chunks = _chunk_days(ordered, no_of_days_to_stay, per_day=per_day)

    trip_plan: List[Dict[str, Any]] = []
    for day_idx, day_list in enumerate(day_chunks, start=1):
        locs = []
        for day_item_idx, item in enumerate(day_list):
            idx = ordered.index(item)
            dist_val = distances_km[idx] if idx < len(distances_km) else None
            travel_duration = travel_durations_min[idx] if idx < len(travel_durations_min) else None
            
            # Format distance string
            if day_item_idx == 0:  # First item of each day
                dist_str = "0.0 km"  # First item of each day starts fresh
                travel_str = "0 min"
            elif isinstance(dist_val, (int, float)):
                dist_str = f"{dist_val:.1f} km"
                if isinstance(travel_duration, int):
                    travel_str = _format_duration(travel_duration)
                else:
                    travel_str = "N/A"
            else:
                dist_str = "N/A"  # Fallback when distance calculation fails
                travel_str = "N/A"
            
            # Estimate visit duration based on place types and name
            visit_duration_min = _estimate_visit_duration(
                item.get("types", []), 
                item["name"]
            )
            visit_duration_str = _format_duration(visit_duration_min)
                
            locs.append(
                {
                    "name": item["name"],
                    "description": item.get("description") or "A popular attraction worth visiting",  # Fallback description
                    "lat": item["lat"],
                    "lng": item["lon"],
                    "photo_url": item.get("photo_url"),
                    "distance_from_previous": dist_str,
                    "travel_duration": travel_str,
                    "estimated_visit_duration": visit_duration_str,
                    "rating": item.get("rating"),
                    "types": item.get("types", []),
                }
            )
        trip_plan.append({"day": day_idx, "locations": locs})

    # Generate stay plan if budget is provided and positive
    stay_plan = []
    if budget is not None and budget > 0:
        try:
            stay_plan = get_stay_plan_suggestions(
                location=location,
                budget=budget_usd,  # Use USD-converted budget for internal processing
                budget_currency=original_currency,
                display_currency=display_currency,
                language=language,
                region=region
            )
        except Exception:
            # If stay plan generation fails, continue with empty stay plan
            pass

    return {"trip_plan": trip_plan, "stay_plan": stay_plan}



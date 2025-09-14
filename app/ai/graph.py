from __future__ import annotations
from typing import Any, Dict, List, Iterator
from uuid import uuid4

from app.ai.state import GraphState
from app.ai.tools import tool_search_hotels, tool_search_flights, tool_search_poi
from app.ai.gemini import gemini_json
from app.schemas.itinerary import Itinerary, DayPlan, Activity
from app.schemas.search import HotelSearchRequest, FlightSearchRequest, PoiSearchRequest
from app.schemas.common import DateRange, Location, Money, Currency
from app.services.geo import enrich_location


def _emit(events: List[Dict[str, Any]], name: str, **payload: Any) -> None:
    events.append({"event": name, **payload})


class PlannerRunner:
    """A simple, linear planner runner.

    This is a placeholder for a LangGraph implementation. It executes a
    deterministic sequence of nodes and emits node-level events. It does not
    stream partial text; only node transitions and final result.
    """

    def run(self, state: GraphState, events: List[Dict[str, Any]]) -> Itinerary:
        # Parse/validate inputs (assumes TripCreateRequest-like fields already provided)
        _emit(events, "node_started", node="resolve_inputs")
        if not state.destinations:
            raise ValueError("At least one destination is required")
        # Enrich destination(s) with lat/lon and dest_id if missing
        enriched_dests: List[Location] = []
        for d in state.destinations:
            enriched_dests.append(enrich_location(d))
        state.destinations = enriched_dests
        # Enrich origin as well if present
        if state.origin:
            state.origin = enrich_location(state.origin)
        nights = state.nights
        if nights is None and state.date_range:
            nights = (state.date_range.end - state.date_range.start).days
        nights = nights or 3
        _emit(events, "node_completed", node="resolve_inputs", nights=nights)

        # Retrieve POIs (best-effort; only if coords available)
        _emit(events, "node_started", node="retrieve_pois")
        poi_items: List[Dict[str, Any]] = []
        dest0 = state.destinations[0]
        if dest0 and dest0.lat is not None and dest0.lon is not None:
            poi_req = PoiSearchRequest(location=dest0)
            poi_res = tool_search_poi(poi_req)
            poi_items = poi_res.get("items", [])
        state.poi_candidates = poi_items
        _emit(events, "node_completed", node="retrieve_pois", items=len(poi_items))

        # Plan days (use LLM only; no heuristic fallback)
        _emit(events, "node_started", node="plan_days")
        day_plans: List[DayPlan] = []
        used_gemini = False
        try:
            day_plans = self._plan_days_with_gemini(state, nights)
            used_gemini = True
        except Exception as e:
            _emit(events, "error", message=f"LLM planning failed: {e}")
            # Surface failure and stop the run
            raise
        state.day_plans = day_plans
        _emit(events, "node_completed", node="plan_days", days=len(day_plans), llm=used_gemini)

        # Search hotels (optional; if dates provided)
        _emit(events, "node_started", node="search_hotels")
        hotel_opts: List[Dict[str, Any]] = []
        if state.date_range:
            h_req = HotelSearchRequest(
                destination=dest0,
                dates=state.date_range,
                rooms=1,
                adults=2,
                children=0,
                currency=state.currency or "INR",
            )
            h_res = tool_search_hotels(h_req)
            hotel_opts = h_res.get("options", [])[:5]
        state.hotel_options = hotel_opts
        _emit(events, "node_completed", node="search_hotels", options=len(hotel_opts))

        # Flights (defer; return sample if origin/dates exist)
        _emit(events, "node_started", node="search_flights")
        flight_opts: List[Dict[str, Any]] = []
        if state.origin and state.date_range:
            f_req = FlightSearchRequest(
                origin=state.origin,
                destination=dest0,
                dates=DateRange(start=state.date_range.start, end=state.date_range.start),
                adults=1,
                currency=state.currency or "INR",
            )
            flight_opts = tool_search_flights(f_req).get("options", [])
        state.flight_options = flight_opts
        _emit(events, "node_completed", node="search_flights", options=len(flight_opts))

        # Finalize itinerary
        _emit(events, "node_started", node="finalize_itinerary")
        itinerary = Itinerary(
            id=str(uuid4()),
            trip_title="Your Trip",
            origin=state.origin,
            destinations=state.destinations,
            traveler=None,  # type: ignore - will be filled by API layer if needed
            constraints=None,  # type: ignore - provided at creation endpoint
            days=day_plans,
            offers=[],
            status="ready",
        )
        _emit(events, "node_completed", node="finalize_itinerary")
        return itinerary

    def _plan_days_with_gemini(self, state: GraphState, nights: int) -> List[DayPlan]:
        # Build a compact POI list for the prompt
        poi_items = state.poi_candidates or []
        poi_lines = []
        for p in poi_items[:60]:
            name = p.get("name") or "POI"
            cat = p.get("category") or "attraction"
            rating = p.get("score") or p.get("rating") or ""
            poi_lines.append(f"- {name} | {cat} | rating {rating}")

        dest_label = state.destinations[0].city or state.destinations[0].country or "the destination"
        pace = state.pace or "relaxed"
        interests = ", ".join(state.interests) if state.interests else "general highlights"
        must_do = ", ".join(state.must_do) if state.must_do else ""

        schema_hint = (
            "Return ONLY JSON with: {\n"
            "  \"day_plans\": [\n"
            "    {\n"
            "      \"summary\": string,\n"
            "      \"activities\": [ { \"name\": string, \"category\": string } ]\n"
            "    }\n"
            "  ]\n"
            "}"
        )

        prompt = (
            f"You are a trip planning assistant.\n"
            f"Plan a {nights}-day trip in {dest_label} for a {pace} pace.\n"
            f"Interests: {interests}.\n"
            + (f"Must-do: {must_do}.\n" if must_do else "")
            + "Select 4-6 realistic attractions per day from this list (avoid repeats):\n"
            + "\n".join(poi_lines)
            + "\nFocus on geographic clustering and reasonable daily flow.\n"
            + schema_hint
        )

        data = gemini_json(prompt)
        raw_days = data.get("day_plans") or []

        # Map POIs by lower-cased name to recover lat/lon when possible
        by_name = {str((p.get("name") or "")).strip().lower(): p for p in poi_items}

        plans: List[DayPlan] = []
        for idx, rd in enumerate(raw_days[:nights]):
            acts: List[Activity] = []
            for a in (rd.get("activities") or [])[:8]:
                aname = str(a.get("name") or "Attraction").strip()
                cat = a.get("category") or "attraction"
                p = by_name.get(aname.lower())
                loc = Location(lat=(p or {}).get("lat"), lon=(p or {}).get("lon")) if p else None
                acts.append(
                    Activity(
                        id=str(uuid4()),
                        name=aname,
                        category=cat,
                        location=loc,
                        notes="Planned by Gemini",
                        source="gemini",
                    )
                )
            plans.append(
                DayPlan(
                    index=idx,
                    date=(state.date_range.start if state.date_range else None),
                    summary=rd.get("summary") or f"Day {idx+1} in {dest_label}",
                    activities=acts,
                    pinned=False,
                )
            )

        # If Gemini returned fewer days, pad with empty placeholders
        while len(plans) < nights:
            plans.append(
                DayPlan(index=len(plans), summary=f"Day {len(plans)+1} in {dest_label}", activities=[])
            )

        return plans

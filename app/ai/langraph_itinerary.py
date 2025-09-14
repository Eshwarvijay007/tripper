from __future__ import annotations
from typing import Any, Dict, List, Optional, Union

from typing_extensions import TypedDict
from langgraph.graph import StateGraph, END

from app.ai.gemini import gemini_json
from app.providers import google_places
from app.services.geo import enrich_location
from app.ai.tools import tool_search_poi, tool_search_hotels, tool_search_flights
from app.schemas.search import PoiSearchRequest, HotelSearchRequest, FlightSearchRequest
from app.schemas.common import DateRange, Location
from app.schemas.itinerary import DayPlan, Activity, Itinerary
from uuid import uuid4


class PlanState(TypedDict, total=False):
    # Inputs
    user_text: Optional[str]
    origin: Optional[dict]
    destinations: List[dict]
    date_range: Optional[dict]
    nights: Optional[int]
    interests: List[str]
    pace: Optional[str]
    with_kids: bool
    must_do: List[str]
    avoid: List[str]
    currency: Optional[str]

    # Working
    poi_candidates: List[dict]
    day_plans: List[dict]
    hotel_options: List[dict]
    flight_options: List[dict]
    disambiguate_options: List[dict]

    # Control
    need_info: bool
    questions: List[str]
    error: Optional[str]


def node_parse_intent(state: PlanState) -> PlanState:
    text = state.get("user_text") or ""
    if not text.strip():
        return state
    prompt = (
        "Extract a trip request into JSON with keys: origin(city?), destinations([city?]), "
        "date_range({start,end} ISO-8601) or nights(number), interests([string]), pace(relaxed|packed), currency. "
        "Return ONLY JSON. If a field is not explicitly present, omit it or set it to null. "
        "Do NOT guess or fabricate missing values. If nights is not provided, omit it (do not default)."
    )
    try:
        data = gemini_json(f"{text}\n\n{prompt}")
        # Merge extracted fields conservatively
        if (dests := data.get("destinations")):
            state["destinations"] = dests
        if (orig := data.get("origin")):
            state["origin"] = orig
        if (dr := data.get("date_range")):
            state["date_range"] = dr
        if (nights := data.get("nights")) is not None:
            try:
                n = int(nights)
            except Exception:
                n = None
            if n is not None and 1 <= n <= 21:
                state["nights"] = n
            else:
                # unset suspicious values to force a follow-up question later
                state.pop("nights", None)
        if (ints := data.get("interests")):
            state["interests"] = ints
        if (pace := data.get("pace")):
            state["pace"] = pace
        if (cur := data.get("currency")):
            state["currency"] = cur
    except Exception:
        # Non-fatal; continue with existing fields
        pass
    # Fallback: if still missing destinations, try to resolve via Google Places
    if not (state.get("destinations") or []) and text.strip():
        try:
            data2 = google_places.text_search_v1(text, limit=5)
            items = data2.get("items", [])
            # If multiple candidates with same name across different countries, prepare disambiguation
            if items:
                name_lower = (items[0].get("name") or "").strip().lower()
                options: List[dict] = []
                seen = set()
                for it in items:
                    nm = (it.get("name") or "").strip()
                    if nm.lower() != name_lower:
                        continue
                    country = it.get("country") or ""
                    key = f"{nm}|{country}"
                    if key in seen:
                        continue
                    seen.add(key)
                    options.append({
                        "city": it.get("city_name") or nm,
                        "country": country,
                        "lat": it.get("lat"),
                        "lon": it.get("lon"),
                    })
                if len(options) > 1:
                    state["disambiguate_options"] = options
                # Default pick first for continuity; may be replaced after user clarifies
                it0 = items[0]
                state["destinations"] = [{
                    "city": it0.get("city_name") or it0.get("name"),
                    "country": it0.get("country"),
                    "lat": it0.get("lat"),
                    "lon": it0.get("lon"),
                }]
        except Exception:
            # ignore
            pass
    return state


def node_check_missing(state: PlanState) -> PlanState:
    qs: List[str] = []
    # Disambiguation question takes priority
    opts = state.get("disambiguate_options") or []
    if opts:
        name = (state.get("destinations") or [{}])[0].get("city") or "this place"
        labels = []
        for o in opts[:5]:
            city = o.get("city") or name
            country = o.get("country") or ""
            labels.append(f"{city}{(', ' + country) if country else ''}")
        qs.append(f"There are multiple places named '{name}'. Which one do you mean? " + ", ".join(labels) + ".")
        state["need_info"] = True
        state["questions"] = qs
        return state
    dests = state.get("destinations") or []
    if not dests:
        qs.append("Where do you want to go?")
    has_date_range = bool(state.get("date_range"))
    # sanity-check nights and invalidate obviously invalid values while keeping LLM in control
    nval = state.get("nights")
    try:
        nint = int(nval) if nval is not None else None
    except Exception:
        nint = None
    if nint is not None and (nint < 1 or nint > 365):
        nint = None
    if nint is None:
        state.pop("nights", None)
    has_nights = nint is not None
    if not has_date_range:
        if has_nights:
            qs.append("What dates do you plan to travel?")
        else:
            qs.append("What are your dates or how many nights (1-21)?")
    if qs:
        state["need_info"] = True
        state["questions"] = qs
    else:
        state["need_info"] = False
        state["questions"] = []
    return state


def _to_location(value: Union[dict, str, None]) -> Optional[Location]:
    if value is None:
        return None
    if isinstance(value, dict):
        return Location(**value)
    if isinstance(value, str):
        # Treat bare strings as city names
        return Location(city=value)
    return None


def node_enrich(state: PlanState) -> PlanState:
    # Enrich origin/destinations with lat/lon when possible using Google/Booking
    raw_dests = state.get("destinations") or []
    dests: List[dict] = []
    for d in raw_dests:
        loc = _to_location(d)
        if loc is not None:
            dests.append(enrich_location(loc).model_dump())
    state["destinations"] = dests
    if (orig := state.get("origin")) is not None:
        oloc = _to_location(orig)
        if oloc is not None:
            state["origin"] = enrich_location(oloc).model_dump()
    return state


def node_retrieve_pois(state: PlanState) -> PlanState:
    poi_items: List[dict] = []
    dests = state.get("destinations") or []
    if dests:
        d0 = dests[0]
        if d0.get("lat") is not None and d0.get("lon") is not None:
            req = PoiSearchRequest(location=Location(**d0))
            poi_items = tool_search_poi(req).get("items", [])
    state["poi_candidates"] = poi_items
    return state


def node_plan_days(state: PlanState) -> PlanState:
    # Prefer Gemini JSON; fall back to heuristic
    poi_items = state.get("poi_candidates") or []
    nights = state.get("nights")
    if nights is None and state.get("date_range"):
        dr = DateRange(**state["date_range"])  # type: ignore
        nights = (dr.end - dr.start).days
    try:
        nights = int(nights) if nights is not None else None
    except Exception:
        nights = None
    # Do not impose artificial caps here; if still None, let the planner prompt decide
    dests = state.get("destinations") or []
    dest_label = (dests[0].get("city") if dests else None) or (dests[0].get("country") if dests else None) or "destination"

    # Try LLM planning
    try:
        # Build a compact POI list for the prompt
        poi_lines = []
        for p in poi_items[:60]:
            name = p.get("name") or "POI"
            cat = p.get("category") or "attraction"
            rating = p.get("score") or p.get("rating") or ""
            poi_lines.append(f"- {name} | {cat} | rating {rating}")

        pace = state.get("pace") or "relaxed"
        interests = ", ".join(state.get("interests") or []) or "general highlights"
        must_do = ", ".join(state.get("must_do") or [])
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
        by_name = {str((p.get("name") or "")).strip().lower(): p for p in poi_items}
        plans: List[dict] = []
        for idx, rd in enumerate(raw_days[:nights]):
            acts: List[dict] = []
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
                    ).model_dump()
                )
            plans.append(
                DayPlan(index=idx, summary=rd.get("summary") or f"Day {idx+1} in {dest_label}", activities=[Activity(**a) for a in acts]).model_dump()
            )
        while len(plans) < nights:
            plans.append(DayPlan(index=len(plans), summary=f"Day {len(plans)+1} in {dest_label}", activities=[]).model_dump())
        state["day_plans"] = plans
        return state
    except Exception as e:
        # Do not apply heuristic fallback; surface an actionable message instead
        state["day_plans"] = []
        state["need_info"] = True
        state["questions"] = [
            f"LLM planning failed. Please try again or adjust your request. ({str(e)})"
        ]
        state["error"] = f"LLM planning failed: {str(e)}"
        return state


def node_search_hotels(state: PlanState) -> PlanState:
    dests = state.get("destinations") or []
    if not dests or not state.get("date_range"):
        state["hotel_options"] = []
        return state
    h_req = HotelSearchRequest(
        destination=Location(**dests[0]),
        dates=DateRange(**state["date_range"]).model_dump(),  # type: ignore
        rooms=1,
        adults=2,
        children=0,
        currency=state.get("currency") or "USD",
    )
    # Pydantic models not expected here; adapt:
    h_req = HotelSearchRequest(**h_req.model_dump())
    res = tool_search_hotels(h_req)
    state["hotel_options"] = (res.get("options") or [])[:5]
    return state


def node_finalize(state: PlanState) -> PlanState:
    # Marker node; actual persistence is handled by the service layer
    return state


def build_graph() -> StateGraph:
    sg = StateGraph(PlanState)
    sg.add_node("parse_intent", node_parse_intent)
    sg.add_node("check_missing", node_check_missing)
    sg.add_node("enrich", node_enrich)
    sg.add_node("retrieve_pois", node_retrieve_pois)
    sg.add_node("plan_days", node_plan_days)
    sg.add_node("search_hotels", node_search_hotels)
    sg.add_node("finalize", node_finalize)

    sg.set_entry_point("parse_intent")
    sg.add_edge("parse_intent", "check_missing")

    def route_after_check(state: PlanState):
        return END if state.get("need_info") else "enrich"

    sg.add_conditional_edges("check_missing", route_after_check, {END: END, "enrich": "enrich"})
    sg.add_edge("enrich", "retrieve_pois")
    sg.add_edge("retrieve_pois", "plan_days")
    sg.add_edge("plan_days", "search_hotels")
    sg.add_edge("search_hotels", "finalize")
    sg.add_edge("finalize", END)
    return sg

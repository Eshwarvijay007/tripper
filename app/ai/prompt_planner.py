from __future__ import annotations
from typing import Any, Dict, List, Optional
from uuid import uuid4

from app.ai.gemini import gemini_json
from app.schemas.common import Location, DateRange, Money, Currency
from app.schemas.search import HotelSearchRequest, FlightSearchRequest, PoiSearchRequest
from app.schemas.itinerary import Itinerary, DayPlan, Activity
from app.ai.tools import tool_search_hotels, tool_search_flights, tool_search_poi


SYSTEM_SPEC = (
    "You are Layla, an expert travel planning agent.\n"
    "Goal: Orchestrate tool calls and produce a realistic itinerary.\n"
    "Rules:\n"
    "- Never repeat questions about fields that are already known.\n"
    "- Ask only for truly missing items, at most 1-2 concise questions per turn.\n"
    "- Prefer tools to reduce uncertainty (POIs before planning, hotels after dates).\n"
    "- Keep itinerary days reasonable (4-6 activities), cluster by area, avoid repeats.\n"
    "- Return strict JSON only (no prose).\n\n"
    "Tools (inputs -> outputs):\n"
    "- search_poi: { location: { city?, country?, lat?, lon? } } -> { items: [ { id, name, category, lat?, lon?, score?, photo? } ] }\n"
    "- search_hotels: { location: { city?, country?, lat?, lon? }, date_range: { start, end }, currency? } -> { options: [ { id, name, stars?, neighborhood?, price_per_night:{amount,currency}, photo? } ] }\n"
    "- search_flights: { origin: { city?, country?, lat?, lon? }, destination: { city?, country?, lat?, lon? }, date: YYYY-MM-DD, currency? } -> { options: [ ... ] }\n\n"
    "Ask format: { action: 'ask', questions: [string], need_keys: [string] }\n"
    "Tool format: { action: 'tool', name: 'search_poi|search_hotels|search_flights', args: {..} }\n"
    "Finalize format: { action: 'finalize', itinerary: { trip_title: string, days: [ { summary, activities:[{name,category}] } ] } }\n"
)


def _summarize_state(state: Dict[str, Any]) -> str:
    def fmt_loc(d: Optional[Dict[str, Any]]) -> str:
        if not d:
            return "null"
        city = d.get("city") or ""
        country = d.get("country") or ""
        lat = d.get("lat")
        lon = d.get("lon")
        parts = []
        if city:
            parts.append(city)
        if country:
            parts.append(country)
        if lat is not None and lon is not None:
            parts.append(f"({lat}, {lon})")
        return ", ".join([p for p in parts if p]) or "unknown"

    lines = []
    lines.append(f"origin: {fmt_loc(state.get('origin'))}")
    dests = state.get("destinations") or []
    if isinstance(dests, list):
        lines.append("destinations: [" + "; ".join(fmt_loc(d) for d in dests[:3]) + (
            "]" if len(dests) <= 3 else "; …]")
        )
    dr = state.get("date_range") or {}
    lines.append(f"date_range: {dr.get('start')} -> {dr.get('end')}")
    lines.append(f"nights: {state.get('nights')}")
    ints = state.get("interests") or []
    lines.append("interests: " + ", ".join(ints))
    if state.get("poi_candidates"):
        lines.append(f"poi_items: {len(state.get('poi_candidates') or [])}")
    if state.get("hotel_options"):
        lines.append(f"hotel_options: {len(state.get('hotel_options') or [])}")
    return "\n".join(lines)


def _decision_prompt(state: Dict[str, Any]) -> str:
    # Compute missing keys explicitly to help the model avoid repeats
    required_top = ["destinations", "date_range_or_nights"]
    optional_top = ["origin", "currency", "interests", "pace", "with_kids", "must_do", "avoid"]
    missing: List[str] = []
    if not (state.get("destinations") or []):
        missing.append("destinations")
    has_dr = bool((state.get("date_range") or {}).get("start") and (state.get("date_range") or {}).get("end"))
    has_nights = state.get("nights") is not None
    if not (has_dr or has_nights):
        missing.append("date_range_or_nights")
    for k in optional_top:
        if state.get(k) in (None, [], ""):
            # optional; don't force, but list for awareness
            pass
    asked = set([str(x) for x in (state.get("asked_keys") or [])])
    # Remove already-asked from missing to discourage repeats
    missing = [m for m in missing if m not in asked]

    return (
        SYSTEM_SPEC
        + "\nKnown state (do not re-ask these):\n"
        + _summarize_state(state)
        + "\nMissing (ask only from this minimal set):\n- "
        + "\n- ".join(missing or ["none"])
        + ("\nAlready asked (avoid repeating):\n- " + "\n- ".join(list(asked)) if asked else "")
        + "\n\nDecide the next action following the formats above."
    )


class PromptFirstPlanner:
    """Iterative, prompt-first planner that lets the LLM drive orchestration.

    It maintains a lightweight state dict and repeatedly asks the model to
    choose the next action (ask, tool, finalize). Tool results are folded back
    into the state and exposed in the next step's context.
    """

    def __init__(self, max_steps: int = 8) -> None:
        self.max_steps = max_steps

    def run(self, init_state: Dict[str, Any]) -> Dict[str, Any]:
        state: Dict[str, Any] = {k: v for k, v in init_state.items() if v is not None}
        state.setdefault("currency", "USD")

        for _ in range(self.max_steps):
            decision = gemini_json(_decision_prompt(state))
            action = (decision.get("action") or "").strip().lower()
            if action == "ask":
                qs = decision.get("questions") or []
                need_keys = decision.get("need_keys") or []
                # track asked keys to avoid repetition on subsequent steps/turns
                asked = state.setdefault("asked_keys", [])  # type: ignore
                if isinstance(asked, list):
                    for k in need_keys:
                        if k not in asked:
                            asked.append(k)
                return {
                    **state,
                    "need_info": True,
                    "questions": qs,
                }
            if action == "finalize":
                iti = decision.get("itinerary") or {}
                return self._to_final_state(state, iti)
            if action == "tool":
                name = (decision.get("name") or "").strip()
                args = decision.get("args") or {}
                self._run_tool(state, name, args)
                continue
            # Fallback: ask for clarification if model returned something unexpected
            return {
                **state,
                "need_info": True,
                "questions": ["Could you clarify your destination and dates?"]
            }

        # If loop exhausted, try to finalize minimally with any data we have
        return self._to_final_state(state, {"trip_title": "Your Trip", "days": []})

    def _run_tool(self, state: Dict[str, Any], name: str, args: Dict[str, Any]) -> None:
        if name == "search_poi":
            loc = self._to_location(args.get("location") or {})
            if not loc:
                return
            res = tool_search_poi(PoiSearchRequest(location=loc))
            state["poi_candidates"] = res.get("items", [])
            return
        if name == "search_hotels":
            loc = self._to_location(args.get("location") or {})
            dr = self._to_daterange(args.get("date_range") or {})
            currency = (args.get("currency") or state.get("currency") or "USD")
            if not loc or not dr:
                return
            req = HotelSearchRequest(destination=loc, dates=dr, rooms=1, adults=2, children=0, currency=currency)
            state["hotel_options"] = tool_search_hotels(req).get("options", [])
            return
        if name == "search_flights":
            orig = self._to_location(args.get("origin") or {}) or self._to_location(state.get("origin") or {})
            dest0 = self._to_location(args.get("destination") or {}) or (
                self._to_location((state.get("destinations") or [{}])[0]) if state.get("destinations") else None
            )
            date = (args.get("date") or (state.get("date_range") or {}).get("start"))
            currency = (args.get("currency") or state.get("currency") or "USD")
            if not orig or not dest0 or not date:
                return
            req = FlightSearchRequest(origin=orig, destination=dest0, dates=DateRange(start=date, end=date), adults=1, currency=currency)
            state["flight_options"] = tool_search_flights(req).get("options", [])
            return

    def _to_location(self, d: Any) -> Optional[Location]:
        if not isinstance(d, dict):
            return None
        try:
            return Location(**{k: d.get(k) for k in ("city", "country", "lat", "lon") if k in d})
        except Exception:
            return None

    def _to_daterange(self, d: Any) -> Optional[DateRange]:
        if not isinstance(d, dict):
            return None
        try:
            if not d.get("start") or not d.get("end"):
                return None
            return DateRange(start=d["start"], end=d["end"])
        except Exception:
            return None

    def _to_final_state(self, prior: Dict[str, Any], iti_like: Dict[str, Any]) -> Dict[str, Any]:
        # Map model-suggested day/activities into schema-compatible dicts
        dests = prior.get("destinations") or []
        dest_label = (dests[0].get("city") if dests else None) or (dests[0].get("country") if dests else None) or "destination"
        raw_days = iti_like.get("days") or []
        plans: List[Dict[str, Any]] = []
        for idx, rd in enumerate(raw_days):
            acts: List[Dict[str, Any]] = []
            for a in (rd.get("activities") or [])[:8]:
                name = str(a.get("name") or "Attraction").strip()
                cat = a.get("category") or "attraction"
                acts.append(Activity(id=str(uuid4()), name=name, category=cat, notes="Planned by LLM", source="gemini").model_dump())
            plans.append(
                DayPlan(index=idx, summary=(rd.get("summary") or f"Day {idx+1} in {dest_label}"), activities=[Activity(**a) for a in acts]).model_dump()
            )
        state = {
            **prior,
            "day_plans": plans,
            "need_info": False,
            "questions": [],
        }
        return state

from __future__ import annotations
from typing import List
from uuid import uuid4
from app.ai.gemini import gemini_json
from app.schemas.common import Location, DateRange
from app.schemas.itinerary import DayPlan, Activity
from .state import PlanState


def node_plan_days(state: PlanState) -> PlanState:
    poi_items = state.get("poi_candidates") or []
    nights = state.get("nights")
    if nights is None and state.get("date_range"):
        dr = DateRange(**state["date_range"])  # type: ignore
        nights = (dr.end - dr.start).days
    try:
        nights = int(nights) if nights is not None else None
    except Exception:
        nights = None

    if nights is None or nights <= 0:
        state["need_info"] = True
        state["questions"] = ["Trip length is missing or invalid. Please provide dates or nights (1–21)."]
        state["next"] = "finalize"
        return state

    dests = state.get("destinations") or []
    dest_label = (dests[0].get("city") if dests else None) or (dests[0].get("country") if dests else None) or "destination"
    try:
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
        for idx, rd in enumerate(raw_days[: (nights or 0)]):
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
        state["day_plans"] = plans
        state["next"] = "search_hotels"
        return state
    except Exception as e:
        state["day_plans"] = []
        state["need_info"] = True
        state["questions"] = [
            f"LLM planning failed. Please try again or adjust your request. ({str(e)})"
        ]
        state["error"] = f"LLM planning failed: {str(e)}"
        state["next"] = "finalize"
        return state


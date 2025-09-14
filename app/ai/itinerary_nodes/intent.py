from __future__ import annotations
from typing import List
from app.ai.gemini import gemini_json
from app.providers import google_places
from .state import PlanState


def node_parse_intent(state: PlanState) -> PlanState:
    text = state.get("user_text") or ""
    if not text.strip():
        state["next"] = "check_missing"
        return state
    prompt = (
        "Extract a trip request into JSON with keys: origin(city?), destinations([city?]), "
        "date_range({start,end} ISO-8601) or nights(number), interests([string]), pace(relaxed|packed), currency, "
        "with_kids(boolean?), must_do([string]?), avoid([string]?), budget({amount?,currency?}?). "
        "Return ONLY JSON. If a field is not explicitly present, omit it or set it to null. "
        "Do NOT guess or fabricate missing values. If nights is not provided, omit it (do not default)."
    )
    try:
        data = gemini_json(f"{text}\n\n{prompt}")
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
                state.pop("nights", None)
        if (ints := data.get("interests")):
            state["interests"] = ints
        if (pace := data.get("pace")):
            state["pace"] = pace
        if (cur := data.get("currency")):
            state["currency"] = cur
        if (wk := data.get("with_kids")) is not None:
            try:
                state["with_kids"] = bool(wk)
            except Exception:
                pass
        if (md := data.get("must_do")):
            state["must_do"] = md
        if (av := data.get("avoid")):
            state["avoid"] = av
        if (bd := data.get("budget")):
            state["budget"] = bd
    except Exception:
        pass
    # Fallback: destination disambiguation via Places when user mentions a name
    if not (state.get("destinations") or []) and text.strip():
        try:
            data2 = google_places.text_search_v1(text, limit=5)
            items = data2.get("items", [])
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
                it0 = items[0]
                state["destinations"] = [{
                    "city": it0.get("city_name") or it0.get("name"),
                    "country": it0.get("country"),
                    "lat": it0.get("lat"),
                    "lon": it0.get("lon"),
                }]
        except Exception:
            pass
    state["next"] = "check_missing"
    return state

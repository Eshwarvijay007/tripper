from __future__ import annotations
from typing import TypedDict, List, Annotated, Dict, Any, Optional

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from app.ai.gemini import gemini_json
from app.ai.tools import tool_search_poi, tool_search_hotels
from app.schemas.search import PoiSearchRequest, HotelSearchRequest
from app.schemas.common import Location, DateRange
from app.services.geo import enrich_location


class MessagesState(TypedDict, total=False):
    messages: Annotated[List[AnyMessage], add_messages]
    action: str  # 'assistant' | 'search_poi' | 'search_hotels'
    params: Dict[str, Any]


SYSTEM_PROMPT = (
    "You are Layla, a helpful, concise travel agent. "
    "Clarify dates, origin, budgets, interests, pace, and constraints. "
    "Offer practical suggestions for destinations, day-by-day outlines, "
    "and relevant hotels or attractions when asked. Be specific and friendly."
)


# Gemini 2.5 Pro model via LangChain Google GenAI wrapper.
# Requires env GOOGLE_API_KEY set to a valid key.
_API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
# Use explicit google_api_key to avoid ADC and enforce API-key auth
model = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0.5, google_api_key=_API_KEY)


def assistant_node(state: MessagesState) -> MessagesState:
    msgs = state["messages"]
    # Ensure a system prompt is present at the start of a thread
    if not msgs or not isinstance(msgs[0], SystemMessage):
        msgs = [SystemMessage(content=SYSTEM_PROMPT), *msgs]
    ai = model.invoke(msgs)
    return {"messages": [ai]}


def _last_user_text(state: MessagesState) -> str:
    for m in reversed(state.get("messages", [])):
        if isinstance(m, HumanMessage):
            return str(m.content or "")
    return ""


def router_node(state: MessagesState) -> MessagesState:
    text = _last_user_text(state).strip()
    if not text:
        return {"action": "assistant", "params": {}}
    try:
        spec = (
            "Classify the user's intent for a travel chat. Return ONLY JSON with keys: "
            "action(one of: assistant, search_poi, search_hotels), "
            "location({city?, country?, lat?, lon?}) optional, "
            "date_range({start,end} ISO-8601) optional, currency(optional). "
            "Do not hallucinate; omit unknown fields."
        )
        data = gemini_json(f"{text}\n\n{spec}")
        action = data.get("action") or "assistant"
        params = {k: v for k, v in data.items() if k != "action"}
        return {"action": action, "params": params}
    except Exception:
        return {"action": "assistant", "params": {}}


def search_poi_node(state: MessagesState) -> MessagesState:
    params = state.get("params") or {}
    loc_in = params.get("location") or {}
    loc = None
    if isinstance(loc_in, dict) and (loc_in.get("city") or (loc_in.get("lat") is not None and loc_in.get("lon") is not None)):
        base = Location(**{k: loc_in.get(k) for k in ("city", "country", "lat", "lon") if k in loc_in})
        loc = enrich_location(base)
    # If still no usable location, ask for clarification
    if not loc or loc.lat is None or loc.lon is None:
        msg = AIMessage(content="Which city should I search attractions in?")
        return {"messages": [msg]}
    req = PoiSearchRequest(location=loc)
    res = tool_search_poi(req)
    items = res.get("items", [])
    if not items:
        msg = AIMessage(content=f"I couldn't find attractions around {loc.city or 'that location'}. Try a different area?")
        return {"messages": [msg]}
    lines = []
    for it in items[:10]:
        name = it.get("name") or "Attraction"
        rating = it.get("score")
        lines.append(f"- {name}{(f' (rating {rating})' if rating else '')}")
    text = (
        f"Here are some popular attractions near {loc.city or loc.country}:\n" + "\n".join(lines)
    )
    return {"messages": [AIMessage(content=text)]}


def search_hotels_node(state: MessagesState) -> MessagesState:
    params = state.get("params") or {}
    loc_in = params.get("location") or {}
    dr_in = params.get("date_range") or {}
    currency = params.get("currency") or "USD"
    loc = None
    if isinstance(loc_in, dict) and (loc_in.get("city") or (loc_in.get("lat") is not None and loc_in.get("lon") is not None)):
        base = Location(**{k: loc_in.get(k) for k in ("city", "country", "lat", "lon") if k in loc_in})
        loc = enrich_location(base)
    if not loc:
        return {"messages": [AIMessage(content="Which city should I search hotels in?")]}
    if not isinstance(dr_in, dict) or not dr_in.get("start") or not dr_in.get("end"):
        return {"messages": [AIMessage(content="What are your check-in and check-out dates?")]}
    try:
        dates = DateRange(**dr_in)
    except Exception:
        return {"messages": [AIMessage(content="Please provide dates in YYYY-MM-DD format (check-in and check-out).")]} 
    req = HotelSearchRequest(
        destination=loc,
        dates=dates,
        rooms=1,
        adults=2,
        children=0,
        currency=currency,
    )
    res = tool_search_hotels(req)
    options = res.get("options", [])
    if not options:
        return {"messages": [AIMessage(content=f"I couldn't find hotels for those dates in {loc.city or 'that location'}. Try different dates?")]} 
    lines = []
    for h in options[:5]:
        name = h.get("name") or "Hotel"
        price = ((h.get("price_per_night") or {}).get("amount"))
        curr = ((h.get("price_per_night") or {}).get("currency"))
        stars = h.get("stars")
        parts = [name]
        if stars:
            parts.append(f"{stars}★")
        if price is not None and curr:
            parts.append(f"{price} {curr}/night")
        lines.append(" - ".join(parts))
    text = (
        f"Top hotel options in {loc.city or loc.country} for your dates:\n" + "\n".join(f"- {ln}" for ln in lines)
    )
    return {"messages": [AIMessage(content=text)]}


_builder = StateGraph(MessagesState)
_builder.add_node("route", router_node)
_builder.add_node("assistant", assistant_node)
_builder.add_node("search_poi", search_poi_node)
_builder.add_node("search_hotels", search_hotels_node)
_builder.set_entry_point("route")

def _route_after_route(state: MessagesState) -> str:
    action = state.get("action") or "assistant"
    if action not in {"assistant", "search_poi", "search_hotels"}:
        return "assistant"
    return action

_builder.add_conditional_edges("route", _route_after_route, {
    "assistant": "assistant",
    "search_poi": "search_poi",
    "search_hotels": "search_hotels",
})
_builder.add_edge("assistant", END)
_builder.add_edge("search_poi", END)
_builder.add_edge("search_hotels", END)

# Per-thread in-memory checkpointing
_memory = MemorySaver()
graph = _builder.compile(checkpointer=_memory)

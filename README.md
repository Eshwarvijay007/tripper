
![CodeRabbit Pull Request Reviews](https://img.shields.io/coderabbit/prs/github/Eshwarvijay007/tripper?utm_source=oss&utm_medium=github&utm_campaign=Eshwarvijay007%2Ftripper&labelColor=171717&color=FF570A&link=https%3A%2F%2Fcoderabbit.ai&label=CodeRabbit+Reviews)
Layla Travel Backend (FastAPI Scaffold)
===========================================
This is a scaffolded backend for an AI travel planner in FastAPI. It defines a clean API surface for chat, itinerary planning, and search (flights, hotels, POIs). Auth is bypassed for now.

Quick Start
-----------
- Install: `pip install -r requirements.txt`
- Run: `uvicorn app.main:app --reload`
- Health: `GET http://localhost:8000/api/healthz`

Environment Configuration
-------------------------
Set these env vars when integrating Booking.com via RapidAPI:

- `BOOKING_RAPIDAPI_KEY` — your RapidAPI key (do not commit it)
- `BOOKING_RAPIDAPI_HOST` — default `booking-com15.p.rapidapi.com`
- `BOOKING_RAPIDAPI_BASE` — default `https://booking-com15.p.rapidapi.com`

For Google Places (nearby attractions):

- `GOOGLE_PLACES_API_KEY` — your Google Maps Platform key (Places/Maps JS enabled)

Enable the following Google Maps Platform APIs for the key:
- Places API (Text Search, Nearby Search, Place Photos)
- Maps JavaScript API (if used on the frontend)

If you see empty results from `/api/places/suggest`, verify the key has Places API enabled and is allowed for server-side HTTP requests (no referrer-only restriction). The backend returns 502 with Google error details when the Places API responds with a non-OK status.

For Gemini (LLM planning):

- `GEMINI_API_KEY` — your Google AI Studio API key (or set `GOOGLE_API_KEY`)

API Surface (Initial Draft)
--------------------------
- Chat
  - `POST /api/chat/messages` → start/continue a conversation. Returns `conversation_id`, `message_id`, and `stream_url`.
  - `GET /api/chat/stream/{conversation_id}` → NDJSON stream of stubbed events.

- Itineraries
  - `POST /api/itineraries` (TripCreateRequest) → `202 Accepted` with `JobStatus {id,status,result_type,result_id}`; stub immediately completes and creates a placeholder itinerary.
  - `GET /api/itineraries/{id}` → Itinerary JSON.
  - `PATCH /api/itineraries/{id}` → Shallow updates to title/constraints.
  - `POST /api/itineraries/{id}/regenerate` → `202` JobStatus (stub completes immediately).

- Search
  - `POST /api/search/flights` (FlightSearchRequest) → `options[]` (stubbed Sample Air).
  - `POST /api/search/hotels` (HotelSearchRequest) → `options[]` with paging.
  - `POST /api/search/poi` (PoiSearchRequest) → `items[]` with scores.

- Jobs
  - `GET /api/jobs/{job_id}` → JobStatus.
- Runs (orchestration)
  - `POST /api/runs/itinerary` → start a planning run (stubbed)
  - `GET /api/runs/{id}` → run status
  - `GET /api/runs/{id}/stream` → SSE node/tool events (stubbed)

- Booking (RapidAPI)
  - `GET /api/booking/destinations?query=...` → destination suggestions (maps to Booking searchDestination)

Schemas
-------
- See `app/schemas/*` for Pydantic models (trip creation, itinerary, search, chat, jobs, common types).

Notes & Next Steps
------------------
- Auth: Currently bypassed. Add JWT/session when ready; wire a dependency for optional user context.
- Persistence: In-memory stores (`app/services/store.py`). Replace with Postgres + Redis when implementing.
- LLM/Planning: A background runner executes a simple planner now. Next: integrate LangGraph and Gemini-driven intent parsing/day planning, with hotel/flight/POI tools.
- Streaming: Current stream is NDJSON. Swap to SSE if preferred.
- Validation: Add tighter validation and enums for interests, pace, filters.
- Booking.com hotels: Provide the hotel listing/availability endpoint(s) cURL to wire `/api/search/hotels` to live data. We already support destination resolution via `/api/booking/destinations`.
- Google Places: `/api/search/poi` will return nearby attractions when `location.lat/lon` is provided. Remember to display Places results on a Google Map and follow attribution/retention terms.


Architecture
------------
- API Layer (FastAPI)
  - Routers under `app/api/` expose resources for chat, itineraries, jobs/runs, search, and booking helpers.
  - CORS and env loading are configured in `app/main.py`.

- AI Orchestration (LangGraph, local agents)
  - Itinerary Planner: `app/ai/langraph_itinerary.py` wires a modular graph built from nodes in `app/ai/itinerary_nodes/`.
    - State: `PlanState` (TypedDict with Annotated merge reducers) controls how node outputs merge.
    - Nodes (one per file):
      - `entry` → routes into planning
      - `intent` → parses free text (Gemini JSON) and optional disambiguation via Places
      - `validate` → asks for missing info (need_info + questions)
      - `enrich` → enriches origin/destinations with lat/lon
      - `pois` → retrieves nearby attractions
      - `plan` → builds day plans via Gemini using the POI shortlist (no heuristic fallback)
      - `hotels` → finds stays via Google Places v1 (lodging), fetches details/photos
      - `finalize` → terminal marker
    - Routing style: each node sets `state["next"]`; `add_conditional_edges` uses that to hop between nodes.
    - Execution: compiled locally (no remote service), with a MemorySaver checkpointer for `/api/runs/*` so runs are resumable/traceable.

  - Chat Graph: `app/ai/chat_graph.py` (LangGraph) with Gemini 2.5 Pro
    - Messages state with MemorySaver (keyed by `thread_id`)
    - Router node → either `assistant` (LLM reply) or tool nodes for POIs/hotels
    - Integrated with `/api/chat/messages` + `/api/chat/stream/{conversation_id}` (NDJSON-like streaming)

- Tools & Providers
  - Tools: `app/ai/tools.py`
    - Hotels: Google Places v1 “lodging” + details; falls back to Booking RapidAPI when Places key is missing.
    - POIs: Google Places Nearby (tourist_attraction)
    - Flights: placeholder sample
  - Providers: `app/providers/google_places.py` and `app/providers/booking_rapidapi.py`
    - Places v1 helpers for text search, lodging search, photos, details

- Runs & Streaming
  - Starts in background (`app/services/runs.py`), compiles the itinerary graph with MemorySaver and streams node updates.
  - `/api/runs/{id}/stream` returns SSE of node events; `/api/runs/{id}` returns status; final itinerary persisted in-memory.

- Schemas & Models
  - Pydantic models in `app/schemas/*`: Itinerary, DayPlan, Activity, Location, DateRange, Money, requests/responses.

- Frontend (included under `tripplanner/`)
  - Minimal demo UI (Vite + React) to chat, view itinerary, hotels, attractions, and a map.
  - Hotels now render rich cards (image, title, stars, approx price, description) and a “hero” card for the top-rated stay.

Execution Flow (Itinerary)
- Client calls `POST /api/agent/plan` with `user_text` and/or partial state.
- Graph runs locally:
  - intent → validate → (need_info? return questions) → enrich → pois → plan → hotels → finalize
- Response:
  - If `need_info`: `{ need_info: true, questions[], state }`
  - Else: `{ need_info: false, itinerary, hotel_options[] }`

Key Environment Variables
- LLM (Gemini): `GOOGLE_API_KEY` (or `GEMINI_API_KEY`)
- Google Places: `GOOGLE_PLACES_API_KEY` (or `GOOGLE_MAPS_API_KEY`)
- Booking RapidAPI (fallback): `BOOKING_RAPIDAPI_KEY`, `BOOKING_RAPIDAPI_HOST`, `BOOKING_RAPIDAPI_BASE`
- Optional tracing (LangSmith): `LANGCHAIN_TRACING_V2`, `LANGSMITH_API_KEY`, `LANGCHAIN_PROJECT`

Local Development
- `python -m venv .venv && source .venv/bin/activate`
- `pip install -r requirements.txt`
- Set env in `.env` (LLM + Places keys)
- `uvicorn app.main:app --reload`

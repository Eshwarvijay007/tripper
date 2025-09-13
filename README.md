Layla Travel Backend (FastAPI Scaffold)
===========================================
![CodeRabbit Pull Request Reviews](https://img.shields.io/coderabbit/prs/github/Eshwarvijay007/tripper?utm_source=oss&utm_medium=github&utm_campaign=Eshwarvijay007%2Ftripper&labelColor=171717&color=FF570A&link=https%3A%2F%2Fcoderabbit.ai&label=CodeRabbit+Reviews)
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

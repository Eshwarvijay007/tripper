from __future__ import annotations
from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# Load .env BEFORE importing modules that may read env at import time
load_dotenv()

from .core.config import settings
from .api.health import router as health_router
from .api.itineraries import router as itineraries_router
from .api.search import router as search_router
from .api.chat import router as chat_router
from .api.jobs import router as jobs_router
from .api.runs import router as runs_router
from .api.booking import router as booking_router
from .api.places import router as places_router
from .api.agent import router as agent_router
app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=True,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)

app.include_router(health_router)
app.include_router(itineraries_router)
app.include_router(search_router)
app.include_router(chat_router)
app.include_router(jobs_router)
app.include_router(runs_router)
app.include_router(booking_router)
app.include_router(places_router)
app.include_router(agent_router)


@app.get("/")
def root():
    return {"name": settings.app_name, "environment": settings.environment}

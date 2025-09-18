from __future__ import annotations
import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# Load .env BEFORE importing modules that may read env at import time
load_dotenv()

from .core.config import settings
from .api.health import router as health_router
from .api.chat import router as chat_router
app = FastAPI(title=settings.app_name)

# Serve built frontend (Vite) if available
FRONTEND_DIST = Path(os.getenv("FRONTEND_DIST", "/opt/frontend")).resolve()
INDEX_HTML = FRONTEND_DIST / "index.html"
ASSETS_DIR = FRONTEND_DIST / "assets"

if ASSETS_DIR.exists():
    app.mount("/assets", StaticFiles(directory=str(ASSETS_DIR)), name="assets")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=True,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)

app.include_router(health_router)
app.include_router(chat_router)


@app.get("/")
def root():
    if INDEX_HTML.exists():
        return FileResponse(str(INDEX_HTML))
    return {"name": settings.app_name, "environment": settings.environment}


@app.get("/{full_path:path}")
def spa_fallback(full_path: str):
    # Let API routes 404 through normal handlers
    if full_path.startswith("api/"):
        raise HTTPException(status_code=404)
    if INDEX_HTML.exists():
        return FileResponse(str(INDEX_HTML))
    raise HTTPException(status_code=404)

from __future__ import annotations
from typing import Dict, Any


# Extremely simple in-memory stores for scaffolding only
JOBS: Dict[str, Dict[str, Any]] = {}
ITINERARIES: Dict[str, Dict[str, Any]] = {}
CONVERSATIONS: Dict[str, Dict[str, Any]] = {}
MESSAGES: Dict[str, Dict[str, Any]] = {}
RUNS: Dict[str, Dict[str, Any]] = {}
RUN_EVENTS: Dict[str, list] = {}

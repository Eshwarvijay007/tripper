from __future__ import annotations
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from app.schemas.common import Location, DateRange, Money
from app.schemas.itinerary import DayPlan


class GraphState(BaseModel):
    # Input/Context
    run_id: str
    user_text: Optional[str] = None
    origin: Optional[Location] = None
    destinations: List[Location] = Field(default_factory=list)
    date_range: Optional[DateRange] = None
    nights: Optional[int] = None
    interests: List[str] = Field(default_factory=list)
    pace: Optional[str] = None  # relaxed | packed
    with_kids: bool = False
    must_do: List[str] = Field(default_factory=list)
    avoid: List[str] = Field(default_factory=list)
    budget: Optional[Money] = None
    currency: Optional[str] = "INR"

    # Working data
    poi_candidates: List[Dict[str, Any]] = Field(default_factory=list)
    day_plans: List[DayPlan] = Field(default_factory=list)
    hotel_options: List[Dict[str, Any]] = Field(default_factory=list)
    flight_options: List[Dict[str, Any]] = Field(default_factory=list)
    offers: List[Dict[str, Any]] = Field(default_factory=list)

    # Control/Errors
    errors: List[str] = Field(default_factory=list)


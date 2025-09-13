from __future__ import annotations
from datetime import date, time
from typing import List, Optional
from pydantic import BaseModel, Field

from .common import Money, DateRange, Location


class TravelerInfo(BaseModel):
    adults: int = 2
    children: int = 0
    infants: int = 0


class ItineraryConstraints(BaseModel):
    date_range: Optional[DateRange] = None
    nights: Optional[int] = None
    budget: Optional[Money] = None
    interests: List[str] = []
    pace: Optional[str] = None  # e.g., "relaxed", "packed"
    must_do: List[str] = []
    avoid: List[str] = []
    currency: Optional[str] = "USD"
    locale: Optional[str] = "en"


class TripCreateRequest(BaseModel):
    origin: Optional[Location] = None
    destinations: List[Location] = Field(default_factory=list)
    traveler: TravelerInfo = TravelerInfo()
    constraints: ItineraryConstraints = ItineraryConstraints()
    title: Optional[str] = None


class Activity(BaseModel):
    id: str
    name: str
    category: Optional[str] = None
    location: Optional[Location] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    cost: Optional[Money] = None
    notes: Optional[str] = None
    source: Optional[str] = None


class DayPlan(BaseModel):
    index: int
    date: Optional[date] = None
    summary: Optional[str] = None
    activities: List[Activity] = Field(default_factory=list)
    pinned: bool = False


class Offer(BaseModel):
    id: str
    type: str  # flight | hotel | activity
    partner: Optional[str] = None
    price: Optional[Money] = None
    deeplink: Optional[str] = None


class Itinerary(BaseModel):
    id: str
    trip_title: Optional[str] = None
    origin: Optional[Location] = None
    destinations: List[Location] = Field(default_factory=list)
    traveler: TravelerInfo
    constraints: ItineraryConstraints
    days: List[DayPlan] = Field(default_factory=list)
    offers: List[Offer] = Field(default_factory=list)
    status: str = "ready"  # ready | processing | error
    public_slug: Optional[str] = None


class ItinerarySummary(BaseModel):
    id: str
    trip_title: Optional[str] = None
    days: int
    destinations: List[str] = Field(default_factory=list)


class ItineraryUpdateRequest(BaseModel):
    title: Optional[str] = None
    constraints: Optional[ItineraryConstraints] = None
    add_must_do: List[str] = []
    remove_activities: List[str] = []  # activity ids

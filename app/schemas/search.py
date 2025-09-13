from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, Field
from .common import Location, DateRange, CabinClass, Money, Paging


class FlightSearchRequest(BaseModel):
    origin: Location
    destination: Location
    dates: DateRange
    adults: int = 1
    children: int = 0
    cabin: CabinClass = CabinClass.ECONOMY
    max_price: Optional[float] = None
    currency: str = "USD"


class FlightOption(BaseModel):
    id: str
    carrier: str
    depart_at: str
    arrive_at: str
    duration_minutes: int
    price: Money
    deeplink: Optional[str] = None


class HotelSearchRequest(BaseModel):
    destination: Location
    dates: DateRange
    rooms: int = 1
    adults: int = 2
    children: int = 0
    budget_per_night: Optional[Money] = None
    filters: List[str] = Field(default_factory=list)
    currency: str = "USD"
    paging: Paging = Paging()


class HotelOption(BaseModel):
    id: str
    name: str
    stars: Optional[float] = None
    neighborhood: Optional[str] = None
    price_per_night: Money
    deeplink: Optional[str] = None


class PoiSearchRequest(BaseModel):
    location: Location
    categories: List[str] = Field(default_factory=list)
    with_kids: bool = False
    open_at: Optional[str] = None  # ISO time window
    paging: Paging = Paging()


class Poi(BaseModel):
    id: str
    name: str
    category: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    score: Optional[float] = None


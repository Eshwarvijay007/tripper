from __future__ import annotations
from datetime import date
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class Currency(str, Enum):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    INR = "INR"


class CabinClass(str, Enum):
    ECONOMY = "ECONOMY"
    PREMIUM_ECONOMY = "PREMIUM_ECONOMY"
    BUSINESS = "BUSINESS"
    FIRST = "FIRST"


class Money(BaseModel):
    amount: float
    currency: Currency = Currency.INR


class DateRange(BaseModel):
    start: date
    end: date


class Location(BaseModel):
    city: Optional[str] = None
    country: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    iata: Optional[str] = None  # for flights
    dest_id: Optional[str] = None  # Optional Booking.com destination id
    dest_type: Optional[str] = None  # Optional, e.g., CITY | HOTEL | REGION


class Paging(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=200)

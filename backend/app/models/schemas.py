"""
Pydantic Schemas
================
Request/Response models for the API.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class ChatRequest(BaseModel):
    """User chat message."""
    message: str = Field(..., min_length=1, description="User's travel query")
    session_id: Optional[str] = Field(None, description="Chat session ID for memory")


class ChatResponse(BaseModel):
    """Agent response."""
    reply: str = Field(..., description="Agent's response text")
    session_id: str = Field(..., description="Chat session ID")
    destinations_mentioned: list[str] = Field(default_factory=list)


class DestinationQuery(BaseModel):
    """Search filters for destinations."""
    query: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    continent: Optional[str] = None
    category: Optional[str] = None
    max_budget: Optional[int] = None
    limit: int = Field(10, ge=1, le=50)
    source: str = Field("all", pattern="^(india|world|all)$")


class DestinationResponse(BaseModel):
    """Single destination details."""
    place_name: str
    city: Optional[str] = None
    state: Optional[str] = None
    country: str
    category: str
    rating: float
    description: str
    latitude: float
    longitude: float
    best_time_to_visit: Optional[str] = None
    avg_budget: Optional[float] = None
    currency: str = "USD"
    nearest_airport: Optional[str] = None


class ItineraryRequest(BaseModel):
    """Request to generate an itinerary."""
    destination: str = Field(..., description="Primary destination")
    duration_days: int = Field(3, ge=1, le=30)
    budget: Optional[float] = None
    currency: str = "INR"
    travel_style: str = Field("mid-range", pattern="^(budget|mid-range|luxury)$")
    interests: list[str] = Field(default_factory=list)
    travelers: int = Field(1, ge=1)


class ItineraryDay(BaseModel):
    """Single day in the itinerary."""
    day: int
    title: str
    activities: list[str]
    meals: list[str] = Field(default_factory=list)
    estimated_cost: Optional[float] = None
    tips: list[str] = Field(default_factory=list)


class ItineraryResponse(BaseModel):
    """Generated travel itinerary."""
    destination: str
    duration_days: int
    total_budget: float
    currency: str
    days: list[ItineraryDay]
    accommodation_tips: list[str] = Field(default_factory=list)
    transport_tips: list[str] = Field(default_factory=list)
    packing_list: list[str] = Field(default_factory=list)


class AirportResponse(BaseModel):
    """Airport information."""
    iata_code: str
    airport_name: str
    city: Optional[str] = None
    country: str
    latitude: float
    longitude: float


class StatsResponse(BaseModel):
    """Database statistics."""
    india_destinations: int
    world_destinations: int
    airports: int
    countries: int
    india_states: list[str]
    categories_india: list[str]
    categories_world: list[str]

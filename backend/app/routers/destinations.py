"""
Destinations Router
===================
API endpoints for browsing and searching destinations.
"""

from fastapi import APIRouter, Query
from typing import Optional

from app.models.database import db

router = APIRouter(prefix="/api/destinations", tags=["Destinations"])


@router.get("/india")
async def search_india(
    q: Optional[str] = Query(None, description="Search keyword"),
    state: Optional[str] = Query(None, description="Filter by state"),
    category: Optional[str] = Query(None, description="Filter by category"),
    max_budget: Optional[int] = Query(None, description="Max daily budget INR"),
    limit: int = Query(10, ge=1, le=50),
):
    """Search Indian destinations."""
    results = db.search_india_destinations(
        query=q, state=state, category=category,
        max_budget=max_budget, limit=limit,
    )
    return {"results": results, "count": len(results)}


@router.get("/world")
async def search_world(
    q: Optional[str] = Query(None, description="Search keyword"),
    country: Optional[str] = Query(None, description="Filter by country"),
    continent: Optional[str] = Query(None, description="Filter by continent"),
    category: Optional[str] = Query(None, description="Filter by category"),
    max_budget: Optional[int] = Query(None, description="Max daily budget USD"),
    limit: int = Query(10, ge=1, le=50),
):
    """Search world destinations."""
    results = db.search_world_destinations(
        query=q, country=country, continent=continent,
        category=category, max_budget=max_budget, limit=limit,
    )
    return {"results": results, "count": len(results)}


@router.get("/details/{place_name}")
async def get_details(place_name: str):
    """Get full details for a destination."""
    result = db.get_destination_details(place_name)
    if result:
        return result
    return {"error": f"Destination '{place_name}' not found."}


@router.get("/airports")
async def find_airports(
    city: Optional[str] = Query(None),
    country_code: Optional[str] = Query(None),
    limit: int = Query(5, ge=1, le=20),
):
    """Find airports by city or country."""
    results = db.find_airports(city=city, country_code=country_code, limit=limit)
    return {"results": results, "count": len(results)}


@router.get("/country/{country_name}")
async def get_country(country_name: str):
    """Get country information."""
    result = db.get_country_info(country_name)
    if result:
        return result
    return {"error": f"Country '{country_name}' not found."}


@router.get("/states")
async def list_states():
    """List all Indian states with destinations."""
    return {"states": db.get_all_india_states()}


@router.get("/categories")
async def list_categories(source: str = Query("india", pattern="^(india|world)$")):
    """List all destination categories."""
    return {"categories": db.get_all_categories(source)}


@router.get("/stats")
async def get_stats():
    """Get database statistics."""
    stats = db.get_stats()
    return {
        "india_destinations": stats.get("destinations_india", 0),
        "world_destinations": stats.get("destinations_world", 0),
        "airports": stats.get("airports", 0),
        "countries": stats.get("countries", 0),
        "india_states": db.get_all_india_states(),
        "categories_india": db.get_all_categories("india"),
        "categories_world": db.get_all_categories("world"),
    }

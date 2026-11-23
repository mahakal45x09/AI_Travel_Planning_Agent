"""
Agent Tools
============
LangChain tools that the AI agent can call to search destinations,
get weather, estimate budgets, and find airports.
"""

import json
from typing import Optional
from langchain_core.tools import tool

from app.models.database import db


@tool
def search_destinations(
    query: str,
    source: str = "all",
    category: str = None,
    max_budget: int = None,
    limit: int = 5,
) -> str:
    """Search for travel destinations by keyword, category, or budget.

    Args:
        query: Search term (e.g., "beach", "Rajasthan", "temple", "Europe")
        source: Where to search - "india", "world", or "all"
        category: Filter by category (Heritage, Beach, Hill Station, Nature, etc.)
        max_budget: Maximum daily budget (INR for India, USD for World)
        limit: Number of results to return (default 5)

    Returns:
        JSON string with matching destinations and their details.
    """
    results = []

    if source in ("india", "all"):
        india_results = db.search_india_destinations(
            query=query, category=category, max_budget=max_budget, limit=limit
        )
        for r in india_results:
            r["source"] = "india"
            r["currency"] = "INR"
        results.extend(india_results)

    if source in ("world", "all"):
        world_results = db.search_world_destinations(
            query=query, category=category, max_budget=max_budget, limit=limit
        )
        for r in world_results:
            r["source"] = "world"
            r["currency"] = "USD"
        results.extend(world_results)

    if not results:
        return json.dumps({"message": f"No destinations found for '{query}'. Try a broader search."})

    return json.dumps(results, indent=2, default=str)


@tool
def get_destination_details(place_name: str) -> str:
    """Get detailed information about a specific destination.

    Args:
        place_name: Name of the place (e.g., "Jaipur", "Santorini", "Machu Picchu")

    Returns:
        JSON string with full destination details including description,
        coordinates, budget, best time to visit, and transport info.
    """
    result = db.get_destination_details(place_name)
    if result:
        return json.dumps(result, indent=2, default=str)
    return json.dumps({"error": f"Destination '{place_name}' not found in database."})


@tool
def find_nearest_airports(city: str, country_code: str = None) -> str:
    """Find airports near a city or in a country.

    Args:
        city: City name (e.g., "Mumbai", "Paris", "Tokyo")
        country_code: Optional 2-letter country code (e.g., "IN", "FR", "US")

    Returns:
        JSON string with nearby airports including IATA codes.
    """
    results = db.find_airports(city=city, country_code=country_code, limit=5)
    if results:
        return json.dumps(results, indent=2, default=str)
    return json.dumps({"message": f"No airports found near '{city}'."})


@tool
def get_country_info(country_name: str) -> str:
    """Get country information including currency, language, capital, and more.

    Args:
        country_name: Country name (e.g., "India", "France") or 2-letter code (e.g., "IN")

    Returns:
        JSON string with country details.
    """
    result = db.get_country_info(country_name)
    if result:
        return json.dumps(result, indent=2, default=str)
    return json.dumps({"error": f"Country '{country_name}' not found."})


@tool
def estimate_budget(
    destination: str,
    days: int = 3,
    travel_style: str = "mid-range",
    travelers: int = 1,
) -> str:
    """Estimate travel budget for a destination.

    Args:
        destination: Destination name
        days: Number of days
        travel_style: "budget", "mid-range", or "luxury"
        travelers: Number of travelers

    Returns:
        JSON string with estimated daily and total costs.
    """
    # Get destination info for base budget
    dest_info = db.get_destination_details(destination)

    # Budget multipliers
    style_multipliers = {
        "budget": 0.6,
        "mid-range": 1.0,
        "luxury": 2.5,
    }
    multiplier = style_multipliers.get(travel_style, 1.0)

    if dest_info:
        if dest_info.get("source") == "india":
            base_daily = dest_info.get("avg_budget_per_day_inr", 2500)
            currency = "INR"
        else:
            base_daily = dest_info.get("avg_budget_per_day_usd", 150)
            currency = "USD"
    else:
        # Default estimates
        base_daily = 2500
        currency = "INR"

    daily_cost = base_daily * multiplier
    total_cost = daily_cost * days * travelers

    # Breakdown
    breakdown = {
        "destination": destination,
        "days": days,
        "travelers": travelers,
        "travel_style": travel_style,
        "currency": currency,
        "daily_cost_per_person": round(daily_cost),
        "total_cost": round(total_cost),
        "breakdown": {
            "accommodation": round(daily_cost * 0.40 * days * travelers),
            "food": round(daily_cost * 0.25 * days * travelers),
            "transport": round(daily_cost * 0.20 * days * travelers),
            "activities": round(daily_cost * 0.10 * days * travelers),
            "miscellaneous": round(daily_cost * 0.05 * days * travelers),
        },
        "tips": [
            f"Book accommodation in advance for better rates",
            f"Try local street food for authentic and affordable meals",
            f"Use public transport or shared cabs to save on travel",
        ],
    }

    return json.dumps(breakdown, indent=2)


@tool
def search_india_by_state(state: str, category: str = None) -> str:
    """Search Indian destinations by state.

    Args:
        state: Indian state name (e.g., "Rajasthan", "Kerala", "Himachal Pradesh")
        category: Optional category filter (Heritage, Beach, Hill Station, etc.)

    Returns:
        JSON with destinations in the specified state.
    """
    results = db.search_india_destinations(state=state, category=category, limit=20)
    if results:
        return json.dumps(results, indent=2, default=str)
    return json.dumps({"message": f"No destinations found in '{state}'."})


@tool
def get_database_stats() -> str:
    """Get statistics about available travel data.

    Returns:
        JSON with counts of destinations, airports, countries, and categories.
    """
    stats = db.get_stats()
    states = db.get_all_india_states()
    cat_india = db.get_all_categories("india")
    cat_world = db.get_all_categories("world")

    return json.dumps({
        "total_india_destinations": stats.get("destinations_india", 0),
        "total_world_destinations": stats.get("destinations_world", 0),
        "total_airports": stats.get("airports", 0),
        "total_countries": stats.get("countries", 0),
        "india_states_covered": states,
        "india_categories": cat_india,
        "world_categories": cat_world,
    }, indent=2)


# List of all tools for the agent
ALL_TOOLS = [
    search_destinations,
    get_destination_details,
    find_nearest_airports,
    get_country_info,
    estimate_budget,
    search_india_by_state,
    get_database_stats,
]

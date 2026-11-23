"""
AI Travel Planning Agent — Main Application
=============================================
FastAPI entry point with CORS, routes, and startup initialization.

Usage:
    uvicorn app.main:app --reload --port 8000
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.models.database import db
from app.routers import chat, destinations


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    # --- Startup ---
    print(f"\n🌍 {settings.app_name} v{settings.app_version}")
    print(f"   LLM Provider: {settings.llm_provider}")
    print(f"   LLM Model: {settings.llm_model}")

    # Initialize database with cleaned data
    db.init_db()

    stats = db.get_stats()
    print(f"\n📊 Data loaded:")
    print(f"   India destinations: {stats.get('destinations_india', 0)}")
    print(f"   World destinations: {stats.get('destinations_world', 0)}")
    print(f"   Airports: {stats.get('airports', 0)}")
    print(f"   Countries: {stats.get('countries', 0)}")
    print(f"\n🚀 Server ready at http://{settings.api_host}:{settings.api_port}")
    print(f"📖 API docs at http://localhost:{settings.api_port}/docs\n")

    yield

    # --- Shutdown ---
    db.close()
    print("\n👋 Server shut down.")


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="An intelligent AI travel assistant that creates personalized itineraries "
                "for 190+ countries with deep India coverage.",
    version=settings.app_version,
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router)
app.include_router(destinations.router)


# === Root Endpoints ===

@app.get("/", tags=["Health"])
async def root():
    """Health check and welcome message."""
    return {
        "message": f"🌍 {settings.app_name} is running!",
        "version": settings.app_version,
        "docs": "/docs",
        "endpoints": {
            "chat": "/api/chat/",
            "destinations_india": "/api/destinations/india",
            "destinations_world": "/api/destinations/world",
            "airports": "/api/destinations/airports",
            "stats": "/api/destinations/stats",
        },
    }


@app.get("/health", tags=["Health"])
async def health():
    """Health check endpoint."""
    stats = db.get_stats()
    return {
        "status": "healthy",
        "llm_provider": settings.llm_provider,
        "data_loaded": sum(stats.values()) > 0,
        "stats": stats,
    }

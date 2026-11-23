"""
Configuration Management
========================
Loads environment variables and provides app-wide settings.
"""

import os
from pathlib import Path
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
CLEANED_DATA_DIR = DATA_DIR / "cleaned"
ENV_FILE = PROJECT_ROOT / ".env"

# Load .env file from project root
load_dotenv(ENV_FILE)


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # --- App ---
    app_name: str = "AI Travel Planning Agent"
    app_version: str = "1.0.0"
    debug: bool = True
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # --- LLM Provider ---
    llm_provider: str = "gemini"  # gemini, openai, ollama
    llm_model: str = "gemini-2.0-flash"

    # --- API Keys ---
    google_api_key: str = ""
    openai_api_key: str = ""

    # --- Database ---
    database_url: str = "sqlite:///./travel_agent.db"

    # --- ChromaDB ---
    chroma_persist_dir: str = "./chroma_db"
    chroma_collection_name: str = "travel_destinations"

    # --- External APIs ---
    weather_api_url: str = "https://api.open-meteo.com/v1/forecast"
    exchange_rate_api_key: str = ""

    # --- CORS ---
    frontend_url: str = "http://localhost:5173"
    cors_origins: str = "http://localhost:5173,http://localhost:3000"

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",")]

    class Config:
        env_file = str(ENV_FILE)
        case_sensitive = False


# Global settings instance
settings = Settings()

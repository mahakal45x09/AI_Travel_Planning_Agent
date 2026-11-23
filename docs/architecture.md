# Architecture

## System Overview

```
┌──────────────────────────────────────────────────────┐
│               FRONTEND (React + Vite)                 │
│                                                       │
│   Chat UI ─── Explore Tab ─── About Page              │
│   │                │                                  │
│   └── REST API ────┘                                  │
└──────────┬───────────────────────────────────────────┘
           │ HTTP (port 5173 → 8000)
┌──────────▼───────────────────────────────────────────┐
│              BACKEND (Python FastAPI)                  │
│                                                       │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────┐  │
│  │ Chat Router │  │ Destinations │  │   Health    │  │
│  │ POST /chat/ │  │  GET /india  │  │  GET /      │  │
│  └──────┬──────┘  │  GET /world  │  └─────────────┘  │
│         │         │  GET /stats  │                    │
│         │         └──────────────┘                    │
│         ▼                                             │
│  ┌──────────────────────────────────────────────────┐ │
│  │         LangChain AI Agent                       │ │
│  │                                                  │ │
│  │  System Prompt + Chat Memory (per session)       │ │
│  │         │                                        │ │
│  │         ▼                                        │ │
│  │  Tool Selection → Tool Execution → Response      │ │
│  │                                                  │ │
│  │  Tools:                                          │ │
│  │  ├── search_destinations()                       │ │
│  │  ├── get_destination_details()                   │ │
│  │  ├── find_nearest_airports()                     │ │
│  │  ├── get_country_info()                          │ │
│  │  ├── estimate_budget()                           │ │
│  │  ├── search_india_by_state()                     │ │
│  │  └── get_database_stats()                        │ │
│  └──────────────────────────┬───────────────────────┘ │
│                             │                         │
│  ┌──────────────────────────▼───────────────────────┐ │
│  │           SQLite Database                        │ │
│  │                                                  │ │
│  │  Tables:                                         │ │
│  │  ├── destinations_india (71 rows)                │ │
│  │  ├── destinations_world (40 rows)                │ │
│  │  ├── airports (4,563 rows)                       │ │
│  │  ├── countries (250 rows)                        │ │
│  │  ├── travel_details (139 rows)                   │ │
│  │  └── user_preferences (980 rows)                 │ │
│  └──────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────┘
           │
┌──────────▼───────────────────────────────────────────┐
│               DATA PIPELINE                           │
│                                                       │
│  data/scripts/run_all.py orchestrates:                │
│  ├── clean_airports.py    (85K → 4,563)              │
│  ├── clean_countries.py   (nested → flat)            │
│  ├── clean_travel_details.py (date/cost fixes)       │
│  ├── clean_reviews.py     (category mapping)         │
│  ├── build_india_dataset.py  (curated 71 places)     │
│  └── build_world_dataset.py  (curated 40 places)     │
└───────────────────────────────────────────────────────┘
```

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | React + Vite | Chat UI, destination browser |
| Backend | FastAPI | REST API, CORS, routing |
| AI Agent | LangChain | Tool-calling agent with memory |
| LLM | Gemini / GPT / Ollama | Natural language understanding |
| Database | SQLite | Structured data queries |
| Data Pipeline | Pandas + Python | Cleaning and preparation |

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/chat/` | Send message to AI agent |
| DELETE | `/api/chat/session/{id}` | Clear chat session |
| GET | `/api/destinations/india` | Search India destinations |
| GET | `/api/destinations/world` | Search world destinations |
| GET | `/api/destinations/details/{name}` | Get place details |
| GET | `/api/destinations/airports` | Find airports |
| GET | `/api/destinations/country/{name}` | Get country info |
| GET | `/api/destinations/stats` | Database statistics |
| GET | `/` | Health check |

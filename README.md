# 🦚 AI Travel Planning Agent (TravelBuddy AI)

<div align="center">

**An intelligent AI-powered travel assistant creating personalized itineraries for 190+ countries with deep, culturally rich India coverage.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.0+-61DAFB.svg?logo=react&logoColor=black)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite-5.0+-646CFF.svg?logo=vite&logoColor=white)](https://vitejs.dev/)
[![LangChain](https://img.shields.io/badge/LangChain-0.3+-1C3C3C.svg?logo=langchain&logoColor=white)](https://langchain.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)

<p align="center">
  <em>"अतिथि देवो भव (Atithi Devo Bhava) — Experience the timeless heritage, culture, and wonders of India & the World."</em>
</p>

</div>

---

## 🌟 Highlights & Features

- 🤖 **Conversational AI Agent**: Natural language travel planning with LangChain, powered by Google Gemini (e.g. `gemini-3.1-flash-lite`, `gemini-1.5-flash`) or OpenAI / OpenRouter models.
- 🇮🇳 **Deep Indian Cultural & Heritage Coverage**: 71+ curated destinations across 27 Indian states covering heritage forts, palaces, spiritual ghats, hill stations, and coastal retreats.
- 🌏 **Global Attractions**: 40+ iconic international destinations spanning 6 continents.
- 🎨 **Royal Indian Heritage UI**: Bespoke UI featuring traditional *Jaali* / *Mandala* lattice architectural backgrounds, saffron-temple gold accents, and peacock teal gradients.
- ✈️ **4,500+ Global Airports**: Comprehensive airport search with IATA codes and city mapping.
- 💰 **Intelligent Budget Estimator**: Realistic cost breakdowns across budget, mid-range, and luxury travel styles with accommodation, dining, transport, and activities in INR & USD.
- 📋 **Day-by-Day Itinerary Planner**: Personalized daily itineraries tailored to user preferences, duration, and pace.
- 🔌 **FastAPI REST API**: Fully documented endpoints with Swagger UI at `/docs`.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 Frontend (React + Vite)                     │
│    • Indian Heritage & Jaali UI Theme                       │
│    • Conversational Chat & Streaming Memory                 │
│    • Interactive Exploration & Stats Dashboard              │
└──────────────────────────────┬──────────────────────────────┘
                               │ HTTP / REST API (Port 8000)
┌──────────────────────────────▼──────────────────────────────┐
│                    Backend (FastAPI)                        │
│                                                             │
│   🧠 AI Travel Agent (LangChain Core)                       │
│   ├── Tool Calling & Execution Engine                       │
│   ├── Multi-Session Conversation Memory                     │
│   └── Multi-Provider Support (Gemini / OpenAI / Ollama)     │
│                                                             │
│   🛠️ 7 Integrated Search & Estimation Tools:                │
│   ├── search_destinations()                                 │
│   ├── get_destination_details()                             │
│   ├── find_nearest_airports()                               │
│   ├── estimate_budget()                                     │
│   ├── get_country_info()                                    │
│   ├── search_india_by_state()                               │
│   └── get_database_stats()                                  │
│                                                             │
│   🗃️ Data Layer: SQLite (Indexed Relational Database)       │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+**
- **Node.js 18+** & **npm**
- A **Google Gemini API Key** (from [Google AI Studio](https://aistudio.google.com/)) or an **OpenAI / OpenRouter API Key**

---

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/AI-Travel-Planning-Agent.git
cd AI-Travel-Planning-Agent
```

---

### Step 2: Configure Environment Variables

Copy the `.env.example` file to `.env`:

```bash
cp .env.example .env
```

Open `.env` and set your preferred model configuration:

```env
# --- LLM Provider ---
LLM_PROVIDER=gemini
LLM_MODEL=gemini-3.1-flash-lite

# --- API Keys ---
GOOGLE_API_KEY=your_gemini_api_key_here

# --- Server Settings ---
API_HOST=0.0.0.0
API_PORT=8000
FRONTEND_URL=http://localhost:5173
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

> 💡 **Tip:** Free Gemini API keys can be generated at [Google AI Studio](https://aistudio.google.com/app/apikey). Ensure you select *"Create API key in new project"* to enable the free tier without billing requirements.

---

### Step 3: Set Up and Start the Backend

```bash
cd backend

# Create and activate virtual environment
python -m venv venv

# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the FastAPI server
uvicorn app.main:app --reload --port 8000
```

Backend will be accessible at:
- **API Server:** `http://localhost:8000`
- **Interactive Swagger Docs:** `http://localhost:8000/docs`

---

### Step 4: Set Up and Start the Frontend

In a new terminal window:

```bash
cd frontend

# Install frontend dependencies
npm install

# Start the Vite development server
npm run dev
```

Open your browser at **`http://localhost:5173`** and start planning your journeys! 🎉

---

## 📁 Repository Structure

```
AI_Travel_Planning_Agent/
├── .env.example                  # Template for environment configuration
├── .gitignore                    # Git ignore rules
├── README.md                     # Project documentation
├── backend/
│   ├── requirements.txt          # Python dependencies
│   ├── travel_agent.db           # SQLite database with loaded travel datasets
│   └── app/
│       ├── main.py               # FastAPI entry point & CORS configuration
│       ├── config.py             # Pydantic settings & environment loader
│       ├── agents/
│       │   ├── travel_agent.py   # LangChain agent core & multi-round tool loops
│       │   ├── tools.py          # 7 custom LangChain search & budget tools
│       │   └── prompts.py        # System instructions & persona definitions
│       ├── models/
│       │   ├── database.py       # SQLite connection manager & query methods
│       │   └── schemas.py        # Pydantic request/response schemas
│       └── routers/
│           ├── chat.py           # Chat session & message endpoints
│           └── destinations.py   # Destination, airport & country queries
├── data/
│   ├── cleaned/                  # Production-ready cleaned CSVs
│   │   ├── destinations_india.csv
│   │   ├── destinations_world.csv
│   │   ├── airports_cleaned.csv
│   │   └── countries_cleaned.csv
│   └── scripts/                  # Data ingestion & ETL pipeline scripts
└── frontend/
    ├── package.json              # Frontend dependencies and scripts
    ├── vite.config.js            # Vite configuration
    └── src/
        ├── App.jsx               # React main component (Chat, Explore, About)
        ├── index.css             # Indian heritage theme & Jaali styling
        └── main.jsx              # Application bootstrap
```

---

## 📊 Datasets

| Dataset | Total Records | Details |
|:---|:---:|:---|
| **India Destinations** | 71+ | Curated across 27 Indian states (Heritage, Pilgrimage, Hills, Beaches) |
| **World Destinations** | 40+ | Global iconic landmarks across 6 continents |
| **Airports Database** | 4,563 | International & domestic airports with IATA and city mapping |
| **Countries Database** | 250 | ISO codes, capitals, currencies, languages, and continents |
| **User Preferences** | 980 | TripAdvisor preference mappings |
| **Travel Details** | 139 | In-depth accommodation & trip durations |

To rebuild or re-clean the datasets:
```bash
cd data/scripts
python run_all.py
```

---

## 🔌 API Endpoints Summary

| Method | Endpoint | Description |
|:---|:---|:---|
| `POST` | `/api/chat/` | Send query to AI travel planning agent |
| `DELETE` | `/api/chat/session/{id}` | Clear conversation memory for session |
| `GET` | `/api/destinations/india` | Search India destinations by state, category, budget |
| `GET` | `/api/destinations/world` | Search international destinations |
| `GET` | `/api/destinations/details/{name}` | Fetch full details for a place |
| `GET` | `/api/destinations/airports` | Find nearest airports by city or country |
| `GET` | `/api/destinations/stats` | View loaded destination and airport counts |
| `GET` | `/docs` | Interactive Swagger API documentation |

---

## 🤝 Contributing

Contributions are warmly welcomed! Please check [CONTRIBUTING.md](CONTRIBUTING.md) for details on submitting pull requests, filing bug reports, or proposing new destination datasets.

---

## 👨‍💻 Author & Contact

**Mahakal Ketan Hasmukhbhai**
- 🐙 **GitHub:** [@mahakal45x09](https://github.com/mahakal45x09)
- 💼 **LinkedIn:** [mahakal45x09](https://www.linkedin.com/in/mahakal45x09)
- ✉️ **Email:** [ketanmahakal123@gmail.com](mailto:ketanmahakal123@gmail.com)
- 📁 **Repository:** [AI_Travel_Planning_Agent](https://github.com/mahakal45x09/AI_Travel_Planning_Agent)

---

## 📜 License & Copyright

© 2026 **mahakal45x09** (Mahakal Ketan Hasmukhbhai). All Rights Reserved.  
This project is licensed under the [MIT License](LICENSE).

---

<div align="center">
  <b>Made with ❤️ for travelers exploring Incredible India and the World 🦚</b>
</div>

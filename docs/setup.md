# Setup Guide

## Prerequisites

- **Python 3.10+** — [Download](https://www.python.org/downloads/)
- **Node.js 18+** — [Download](https://nodejs.org/)
- **Git** — [Download](https://git-scm.com/)
- **API Key** (one of):
  - [Google AI Studio](https://aistudio.google.com/) (Gemini — free tier)
  - [OpenAI Platform](https://platform.openai.com/) (GPT — paid)

## Step-by-Step Setup

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/AI-Travel-Planning-Agent.git
cd AI-Travel-Planning-Agent
```

### 2. Configure Environment
```bash
cp .env.example .env
```

Edit `.env` and add your API key:
```env
# For Gemini (recommended — free)
GOOGLE_API_KEY=your_key_here
LLM_PROVIDER=gemini
LLM_MODEL=gemini-2.0-flash

# OR for OpenAI
OPENAI_API_KEY=your_key_here
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o-mini
```

### 3. Run Data Pipeline
```bash
cd data/scripts
python run_all.py
```
This cleans 6 datasets and generates 7 files in `data/cleaned/`.

### 4. Set Up Backend
```bash
cd ../../backend
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 5. Start Backend
```bash
uvicorn app.main:app --reload --port 8000
```
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

### 6. Set Up Frontend
```bash
cd ../frontend
npm install
npm run dev
```
- App: http://localhost:5173

### 7. Start Using!
1. Open http://localhost:5173
2. Click a suggestion chip or type your travel query
3. The AI agent will use its tools to find real data and create your plan

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | Make sure virtual environment is activated |
| `API key error` | Check `.env` has the correct key and provider |
| `CORS error` | Backend runs on 8000, frontend on 5173 (pre-configured) |
| `No data found` | Run `data/scripts/run_all.py` first |
| `Port in use` | Change port: `uvicorn app.main:app --port 8001` |

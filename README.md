# AI Document Analyzer

Upload PDFs and get structured AI-powered summaries with key points, entities, and document classification.

**Live demo:** https://ai-document-analyzer-fgsy.onrender.com

> Note: hosted on Render's free tier, so the first request after inactivity may take 30-60 seconds while services wake up.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React, TypeScript, Vite |
| API Gateway | Node.js, Express, JWT Auth |
| AI Service | Python, FastAPI, OpenAI (gpt-4o-mini) |
| Database | PostgreSQL |
| Infrastructure | Docker Compose, Nginx reverse proxy, Render |

## Architecture

```
Browser → Nginx (:80)
            ├── /        → React SPA (static files)
            └── /api/*   → Node.js Gateway (:3000)
                              └── POST /analyze → FastAPI AI Service (:8000)
                                                      └── OpenAI API

PostgreSQL (:5432) ← Node.js reads/writes
```

The Node.js gateway handles auth, file uploads, and orchestration. The Python AI service is stateless and independently scalable. The AI service supports both OpenAI (production) and Ollama (local development) — it auto-detects based on whether `OPENAI_API_KEY` is set.

## Quick Start

### With Docker (recommended)

```bash
# 1. Clone and configure
git clone https://github.com/IsmailAbb/AI_Document_Analyzer.git
cd AI_Document_Analyzer
cp .env.example .env    # edit JWT_SECRET and add OPENAI_API_KEY

# 2. Launch everything
docker compose up --build

# 3. Open http://localhost
```

### Without Docker (development)

```bash
# Terminal 1 — Database
docker compose up postgres

# Terminal 2 — AI Service
cd ai-service
python -m venv venv && source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...   # or use Ollama by leaving this unset
uvicorn main:app --reload --port 8000

# Terminal 3 — Backend
cd backend
cp .env.example .env   # configure DATABASE_URL, JWT_SECRET, AI_SERVICE_URL
npm install && npm run dev

# Terminal 4 — Frontend
cd frontend
npm install && npm run dev

# Open http://localhost:5173
```

### Local LLM with Ollama (optional)

If you'd rather not use the OpenAI API, the AI service falls back to a local Ollama model when `OPENAI_API_KEY` is unset:

```bash
ollama pull llama3.2:1b
ollama serve
```

## Features

- **JWT Authentication** — Register/login with access tokens
- **PDF Upload** — Drag-and-drop with file type and size validation (10MB limit)
- **AI Analysis** — Extracts summary, key points, entities, and document type
- **Detail Levels** — Choose short, medium, or long analysis depth
- **Real-time Status** — Document cards poll for processing status updates
- **Async Processing** — Upload returns immediately, analysis runs in background

## Project Structure

```
ai-doc-analyzer/
├── frontend/          # React (Vite) SPA
├── backend/           # Node.js / Express API gateway
├── ai-service/        # Python / FastAPI AI microservice
├── nginx/             # Reverse proxy config
├── db/                # SQL schema init script
├── render.yaml        # Render deployment blueprint
└── docker-compose.yml # Full stack orchestration
```

## License

MIT

# AI Document Analyzer

Upload PDFs and get structured AI-powered summaries with key points, entities, and document classification.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React, TypeScript, Vite |
| API Gateway | Node.js, Express, JWT Auth |
| AI Service | Python, FastAPI, Ollama (llama3.2) |
| Database | PostgreSQL |
| Infrastructure | Docker Compose, Nginx reverse proxy |

## Architecture

```
Browser → Nginx (:80)
            ├── /        → React SPA (static files)
            └── /api/*   → Node.js Gateway (:3000)
                              └── POST /analyze → FastAPI AI Service (:8000)
                                                      └── Ollama (host)

PostgreSQL (:5432) ← Node.js reads/writes
```

The Node.js gateway handles auth, file uploads, and orchestration. The Python AI service is stateless and independently scalable. Ollama runs on the host machine for local LLM inference.

## Quick Start

### With Docker (recommended)

```bash
# 1. Clone and configure
git clone https://github.com/IsmailAbb/AI_Document_Analyzer.git
cd AI_Document_Analyzer
cp .env.example .env    # edit JWT_SECRET

# 2. Start Ollama on your machine
ollama pull llama3.2:1b
ollama serve

# 3. Launch everything
docker compose up --build

# 4. Open http://localhost
```

### Without Docker (development)

```bash
# Terminal 1 — Database
docker compose up postgres

# Terminal 2 — AI Service
cd ai-service
python -m venv venv && source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
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
└── docker-compose.yml # Full stack orchestration
```

## License

MIT

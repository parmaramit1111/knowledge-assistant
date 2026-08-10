# Development Setup

## Overview

This guide explains how to set up the Knowledge Assistant development environment locally.

The project consists of:

- **FastAPI** backend
- **React + TypeScript + Vite** frontend
- **PostgreSQL + pgvector** database
- **Ollama or another supported LLM provider**
- **AWS S3** for production document storage

The local development environment does **not require Docker**. Docker is used for containerized deployment and production readiness.

---

# Requirements

Install the following tools:

- Python 3.12+
- Node.js 20+
- npm
- PostgreSQL with pgvector
- Git

Optional:

- Ollama
- Docker

> Docker is not required for normal local development.

---

# Clone the Repository

```bash
git clone <repository-url>

cd knowledge-assistant
```

---

# Automated Setup

The project provides a setup script that prepares the backend and frontend development environments.

```bash
./scripts/setup.sh
```

The script:

- Creates `backend/.venv`
- Installs backend dependencies
- Creates `backend/.env` from `.env.example` when available
- Creates local backend storage
- Installs frontend dependencies
- Creates frontend environment configuration when available

---

# Backend Setup

If you prefer to configure the backend manually:

```bash
cd backend
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

### macOS / Linux

```bash
source .venv/bin/activate
```

### Windows

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Backend Environment Variables

Create the environment file:

```bash
cp .env.example .env
```

Configure the required values.

Example:

```env
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/knowledge_assistant

ENVIRONMENT=development

OLLAMA_BASE_URL=http://localhost:11434
```

The exact variables should follow the current `backend/.env.example`.

**Do not commit `.env` files containing secrets.**

---

# Database

The application uses:

- PostgreSQL
- pgvector
- SQLAlchemy Async
- Alembic

Configure the database connection through:

```env
DATABASE_URL=...
```

Run migrations:

```bash
./scripts/migrate.sh
```

Or manually:

```bash
cd backend

.venv/bin/python -m alembic upgrade head
```

---

# Backend

Start FastAPI manually:

```bash
cd backend

.venv/bin/python -m uvicorn app.main:app --reload
```

The backend will be available at:

```text
http://localhost:8000
```

API documentation:

```text
http://localhost:8000/docs
```

Health endpoint:

```text
http://localhost:8000/api/v1/health
```

---

# Frontend Setup

```bash
cd frontend
```

Install dependencies:

```bash
npm ci
```

Start the development server:

```bash
npm run dev
```

The frontend will normally be available at:

```text
http://localhost:5173
```

---

# Frontend Environment

The frontend uses Vite environment variables.

Example:

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

Only variables prefixed with `VITE_` are exposed to the frontend application.

Do not put secrets or private credentials in frontend environment variables.

---

# Start Full Development Environment

The project provides a convenience script for starting both applications:

```bash
./scripts/start.sh
```

This starts:

```text
React / Vite
    │
    │ :5173
    ▼
FastAPI
    │
    │ :8000
    ▼
PostgreSQL + pgvector
```

The script also provides:

```text
Frontend:
http://localhost:5173

Backend:
http://localhost:8000

API Documentation:
http://localhost:8000/docs

Health:
http://localhost:8000/api/v1/health
```

Press:

```text
Ctrl+C
```

to stop the development services.

---

# Ollama

Ollama is an optional local LLM runtime.

If using Ollama locally, configure:

```env
OLLAMA_BASE_URL=http://localhost:11434
```

The application uses the LLM provider architecture, so Ollama is not required to be part of the core application deployment.

The selected model is configured independently.

Example:

```env
LLM_PROVIDER=ollama
LLM_MODEL=qwen2.5:1.5b
```

Model selection should be based on the deployment requirements and available resources.

---

# Document Storage

## Development

Local development currently supports local storage:

```text
backend/storage/
```

The storage directory is intended for development and testing.

Reset local storage:

```bash
./scripts/reset_storage.sh --force
```

This only removes files from the local storage directory. It does not remove database records.

## Production

Production document storage is planned to use:

```text
AWS S3
```

with a private bucket and restricted IAM permissions.

Production storage should not rely on the container filesystem.

---

# Docker

Docker is supported for containerized deployment.

The project contains:

```text
backend/Dockerfile
frontend/Dockerfile
frontend/nginx.conf
docker-compose.yml
```

Docker is **not required for local development**.

The Docker configuration is intended to provide reproducible application builds for deployment and CI/CD.

---

# Docker Architecture

The current Compose architecture contains:

```text
Frontend
React + Nginx
       │
       ▼
Backend
FastAPI
       │
       ├──────────────► AWS RDS PostgreSQL
       │                    │
       │                    └── pgvector
       │
       └──────────────► LLM Provider
                            │
                            ├── Ollama
                            ├── OpenAI
                            ├── Anthropic
                            └── Gemini
```

PostgreSQL is **not required to run as a Docker service** for the intended deployment architecture.

The production database is expected to use AWS RDS PostgreSQL with pgvector.

---

# Database Migrations

All schema changes must be handled through Alembic migrations.

Create a migration:

```bash
cd backend

.venv/bin/python -m alembic revision --autogenerate -m "describe change"
```

Review the generated migration before applying it.

Apply migrations:

```bash
./scripts/migrate.sh
```

Never modify an already-applied migration in a shared environment.

---

# Health Check

Run:

```bash
./scripts/health-check.sh
```

By default, the script checks:

```text
http://localhost:8000/api/v1/health
```

A different backend can be checked with:

```bash
BACKEND_URL=https://api.example.com ./scripts/health-check.sh
```

---

# Project Scripts

| Script                     | Purpose                               |
| -------------------------- | ------------------------------------- |
| `scripts/setup.sh`         | Prepare local development environment |
| `scripts/start.sh`         | Start frontend and backend locally    |
| `scripts/migrate.sh`       | Run Alembic database migrations       |
| `scripts/health-check.sh`  | Verify backend health                 |
| `scripts/reset_storage.sh` | Reset local development storage       |

---

# Testing

Backend tests:

```bash
cd backend

.venv/bin/python -m pytest
```

Frontend production build:

```bash
cd frontend

npm run build
```

TypeScript validation:

```bash
cd frontend

npx tsc -b
```

---

# API Documentation

When the backend is running:

```text
http://localhost:8000/docs
```

FastAPI also provides the OpenAPI schema through the application.

---

# Development Workflow

Recommended development workflow:

```text
Pull latest changes
        │
        ▼
Create feature branch
        │
        ▼
Run setup if required
        │
        ▼
Start application
        │
        ▼
Implement change
        │
        ▼
Run tests
        │
        ▼
Run frontend build/type check
        │
        ▼
Run health check
        │
        ▼
Commit changes
        │
        ▼
Push branch
        │
        ▼
Create Pull Request
```

---

# Environment Separation

The application should maintain separate configuration for different environments:

```text
Development
    │
    ├── Local PostgreSQL / development RDS
    ├── Local storage
    └── Optional local Ollama

Staging
    │
    ├── AWS RDS
    ├── Private S3
    └── Configured LLM provider

Production
    │
    ├── AWS RDS + pgvector
    ├── Private S3
    └── Client-selected LLM provider
```

Secrets must be supplied through the environment or an appropriate secrets-management mechanism and must never be committed to Git.

---

# Production Deployment

Production deployment is documented separately in:

```text
docs/deployment.md
```

The production deployment documentation will cover:

- Docker
- AWS infrastructure
- RDS
- S3
- LLM runtime
- Environment configuration
- CI/CD
- Application deployment
- Security
- Monitoring
- Health checks

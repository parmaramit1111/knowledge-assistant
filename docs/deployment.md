# Deployment Guide

## Overview

This guide describes how to deploy the Knowledge Assistant using containerized application services and managed AWS infrastructure.

The deployment architecture separates the application runtime from persistent infrastructure:

- **Frontend:** React + Nginx
- **Backend:** FastAPI
- **Database:** AWS RDS PostgreSQL + pgvector
- **Document Storage:** Private AWS S3
- **LLM Runtime:** Ollama or another supported LLM provider
- **Containerization:** Docker
- **Orchestration:** Docker Compose for initial deployment
- **CI/CD:** Planned

The application containers remain stateless wherever possible. Persistent data should be stored in AWS managed services rather than inside application containers.

---

# Deployment Architecture

```text
                         Internet
                            │
                            ▼
                  ┌────────────────────┐
                  │      Frontend      │
                  │    React + Nginx   │
                  │       :80          │
                  └─────────┬──────────┘
                            │
                            ▼
                  ┌────────────────────┐
                  │      Backend       │
                  │      FastAPI       │
                  │       :8000        │
                  └──────┬─────┬───────┘
                         │     │
              ┌──────────┘     └──────────────┐
              ▼                               ▼
     ┌──────────────────┐             ┌──────────────────┐
     │ AWS RDS          │             │ Private AWS S3   │
     │ PostgreSQL       │             │ Document Storage │
     │ + pgvector       │             │                  │
     └──────────────────┘             └──────────────────┘
                         │
                         ▼
                  ┌────────────────────┐
                  │    LLM Provider    │
                  │                    │
                  │ Ollama / OpenAI /  │
                  │ Anthropic / Gemini │
                  └────────────────────┘
```

---

# Deployment Components

## Frontend

The frontend is built using:

- React
- TypeScript
- Vite
- Material UI

The production frontend is compiled into static assets and served by Nginx.

```text
React Source
     │
     ▼
npm run build
     │
     ▼
dist/
     │
     ▼
Nginx
     │
     ▼
HTTP :80
```

The frontend container does not require Node.js at runtime.

---

# Backend

The backend is built using:

- Python 3.12
- FastAPI
- SQLAlchemy Async
- Alembic
- PostgreSQL
- pgvector

The backend container runs:

```text
Uvicorn
    │
    ▼
FastAPI
```

The backend should remain stateless except for temporary/local development storage.

---

# Database

Production database:

```text
AWS RDS PostgreSQL
```

with:

```text
pgvector
```

The application connects through:

```env
DATABASE_URL=postgresql+asyncpg://...
```

The database is not included as a PostgreSQL container in the production Compose architecture.

RDS provides the persistent database layer independently of application containers.

---

# Document Storage

## Production Storage

Uploaded documents should be stored in a **private AWS S3 bucket**.

The application should not depend on the container filesystem for persistent documents.

Recommended logical structure:

```text
documents/
    {document-id}/
        original.pdf

    {document-id}/
        original.docx
```

The S3 bucket should remain private.

Application access should be controlled through AWS IAM permissions.

When users need temporary access to private documents, the backend can generate short-lived presigned URLs.

---

# S3 Security

The production S3 bucket should use:

- Block Public Access
- Server-side encryption
- IAM-based access
- Restricted bucket permissions
- HTTPS/TLS
- Application-controlled object access

AWS credentials should not be committed to the repository.

When deployed on AWS, the preferred approach is to use an IAM role attached to the compute environment rather than hard-coded access keys.

---

# LLM Runtime

The LLM runtime is intentionally separated from the core application.

The backend communicates through the existing LLM provider architecture:

```text
LLMService
    │
    ▼
LLMFactory
    │
    ├── OllamaProvider
    ├── OpenAIProvider
    ├── AnthropicProvider
    └── GeminiProvider
```

This allows the LLM runtime to be selected based on client requirements.

---

# Ollama Deployment

Ollama should not be required as part of the core application Compose stack.

It can run as a separate service or machine.

```text
Knowledge Assistant Backend
          │
          │ OLLAMA_BASE_URL
          ▼
     Ollama Runtime
          │
          ▼
     Selected Model
```

The model should be selected according to:

- Client requirements
- Response quality
- Context requirements
- Available CPU/GPU resources
- Infrastructure cost

A small model can be used for low-cost deployments, while larger models can be provisioned when additional resources are justified.

Model installation should be an explicit deployment operation rather than automatically downloading models during application startup.

---

# Environment Configuration

Environment-specific configuration should be supplied through environment variables.

Example:

```env
ENVIRONMENT=production

DATABASE_URL=postgresql+asyncpg://...

S3_BUCKET_NAME=knowledge-assistant-documents

AWS_REGION=...

LLM_PROVIDER=ollama

LLM_MODEL=qwen2.5:1.5b

OLLAMA_BASE_URL=http://ollama-server:11434
```

The actual configuration should follow the application's environment settings.

Secrets must never be committed to Git.

---

# Docker

The project contains:

```text
backend/Dockerfile
frontend/Dockerfile
frontend/nginx.conf
docker-compose.yml
```

## Backend Image

The backend image:

```text
Python 3.12
    │
    ▼
Install requirements
    │
    ▼
Copy application
    │
    ▼
Run Uvicorn
```

The backend exposes:

```text
8000
```

---

# Frontend Image

The frontend uses a multi-stage Docker build:

```text
Node.js
   │
   ▼
npm ci
   │
   ▼
npm run build
   │
   ▼
dist/
   │
   ▼
Nginx
```

The production container exposes:

```text
80
```

---

# Docker Compose

The current Compose configuration contains:

```text
Frontend
    │
    ▼
Backend
    │
    ├──────────► AWS RDS PostgreSQL
    │
    ├──────────► AWS S3
    │
    └──────────► LLM Provider
```

PostgreSQL is intentionally not defined as a Compose service because production persistence is provided by AWS RDS.

Ollama is also intentionally not defined as a core Compose service because it is an optional, independently provisioned LLM runtime.

---

# Database Migration

Database schema changes are managed through Alembic.

Before deploying a new application version:

```bash
./scripts/migrate.sh
```

The migration process should target the configured environment's `DATABASE_URL`.

For production:

```text
Deployment
    │
    ▼
Run Alembic Migration
    │
    ▼
AWS RDS PostgreSQL
    │
    ▼
Start / Update Backend
```

Database migrations should be reviewed before being applied to production.

---

# Application Deployment

The initial deployment process is:

```text
Build Application
       │
       ▼
Build Docker Images
       │
       ▼
Configure Environment
       │
       ▼
Verify AWS RDS
       │
       ▼
Verify S3
       │
       ▼
Configure LLM Provider
       │
       ▼
Run Database Migration
       │
       ▼
Start Backend
       │
       ▼
Start Frontend
       │
       ▼
Health Check
```

---

# Health Check

The application provides:

```text
GET /api/v1/health
```

The deployment can verify the backend using:

```bash
./scripts/health-check.sh
```

Example:

```text
http://localhost:8000/api/v1/health
```

For a deployed environment:

```bash
BACKEND_URL=https://api.example.com ./scripts/health-check.sh
```

---

# Storage During Deployment

Application containers should be treated as disposable.

Do not depend on:

```text
backend/storage/
```

for production document persistence.

Production documents belong in:

```text
AWS S3
```

The local storage implementation remains useful for:

- Local development
- Testing
- Development without AWS dependencies

---

# Security

Production deployment should follow these principles:

- Private S3 bucket
- S3 Block Public Access enabled
- IAM-based AWS access
- No secrets committed to Git
- HTTPS/TLS
- Restricted database network access
- Restricted application ports
- Environment-specific configuration
- Short-lived document access URLs
- Regular dependency updates
- Container image security scanning

---

# Deployment Environments

The project supports the following conceptual environments:

```text
Development
    │
    ├── Local application
    ├── Local storage
    ├── Development database
    └── Optional Ollama

Staging
    │
    ├── Docker
    ├── AWS RDS
    ├── Private S3
    └── Configured LLM provider

Production
    │
    ├── Docker
    ├── AWS RDS + pgvector
    ├── Private S3
    └── Client-selected LLM provider
```

---

# Deployment Checklist

Before deploying:

```text
[ ] Build backend image
[ ] Build frontend image
[ ] Verify environment variables
[ ] Verify AWS RDS connectivity
[ ] Verify pgvector
[ ] Verify S3 bucket
[ ] Verify IAM permissions
[ ] Configure LLM provider
[ ] Provision required Ollama model if applicable
[ ] Run database migrations
[ ] Start application
[ ] Run health check
[ ] Verify document upload
[ ] Verify document processing
[ ] Verify semantic search
[ ] Verify RAG chat
```

---

# Current Deployment Status

| Component                  | Status          |
| -------------------------- | --------------- |
| Backend Dockerfile         | ✅ Completed    |
| Frontend Dockerfile        | ✅ Completed    |
| Nginx Configuration        | ✅ Completed    |
| Docker Compose             | ✅ Completed    |
| AWS RDS Architecture       | ✅ Defined      |
| Private S3 Architecture    | 🔄 To Implement |
| S3 Storage Provider        | 🔄 To Implement |
| LLM Provider Architecture  | ✅ Completed    |
| Ollama Deployment Strategy | ✅ Defined      |
| Database Migration Script  | ✅ Completed    |
| Health Check Script        | ✅ Completed    |
| CI/CD                      | ⬜ Planned      |
| Production Monitoring      | ⬜ Planned      |

---

# Future Deployment Improvements

The following can be introduced as the project moves toward production:

- CI/CD pipelines
- Container image registry
- Automated deployment
- AWS ECS or equivalent container platform
- Load balancing
- HTTPS certificate management
- Centralized logging
- Application metrics
- Infrastructure monitoring
- Automated database backups
- Automated S3 lifecycle policies
- Container vulnerability scanning
- Deployment rollback strategy

The deployment architecture should evolve incrementally while keeping the application itself provider-independent and stateless.

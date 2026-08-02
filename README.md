# Knowledge Assistant

An enterprise-grade, provider-agnostic Knowledge Assistant built with **FastAPI**, **React**, and a modular **Retrieval-Augmented Generation (RAG)** architecture.

The platform enables organizations to upload documents, build an intelligent knowledge base, and retrieve grounded AI responses using their own data.

---

# Vision

The goal of this project is to build a production-ready enterprise knowledge platform that:

- Supports multiple document formats
- Builds semantic knowledge from uploaded documents
- Generates vector embeddings
- Performs semantic similarity search
- Produces grounded AI responses
- Supports multiple embedding providers
- Supports multiple vector databases
- Supports multiple LLM providers
- Remains modular and provider independent

The architecture is designed around Clean Architecture principles where every processing stage has a single responsibility and can evolve independently.

---

# Current Status

## Completed ✅

### Backend Foundation

- FastAPI
- SQLAlchemy Async
- PostgreSQL
- Alembic
- Generic Repository Pattern
- CQRS
- ExecutionContext
- Workflow Services
- Provider Services
- Background Scheduler
- Global Exception Handling
- Standard API Response
- Request Correlation ID
- Local File Storage

### Document Processing

- Document Upload API
- PDF Parser
- Word (DOCX) Parser
- Text Parser
- HTML Parser
- Markdown Parser
- Parser Factory
- Parsed Document Persistence
- Background Parsing Worker

### Document Chunking

- Recursive Character Splitter
- Chunker Factory
- Document Chunk Persistence
- Background Chunk Worker

---

## In Progress 🚧

- Embedding Generation

---

## Planned

- Vector Database Integration
- Semantic Search
- Prompt Builder
- AI Chat
- Conversation History
- Authentication
- Multi-Tenant Support
- Monitoring
- CI/CD

---

# Processing Pipeline

The backend currently implements the following processing pipeline.

```text
Upload Document
        │
        ▼
Parse Document
        │
        ▼
Chunk Document
        │
        ▼
Embeddings (Upcoming)
        │
        ▼
Vector Database
        │
        ▼
Semantic Retrieval
        │
        ▼
Prompt Builder
        │
        ▼
LLM
        │
        ▼
AI Response
```

---

# Architecture Overview

```text
                HTTP Request
                     │
                     ▼
             FastAPI Controller
                     │
                     ▼
             ExecutionContext
                     │
                     ▼
             Command / Query
                     │
                     ▼
          Workflow Service
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
  Provider Service        Repository
          │
          ▼
     Provider Factory
          │
          ▼
        Provider
```

---

# Background Processing

Long-running operations execute asynchronously.

```text
Scheduler

↓

Worker

↓

ExecutionContext

↓

Command

↓

Workflow Service

↓

Provider Service

↓

Repository
```

Current workers

- DocumentWorker
- ChunkWorker

Future workers

- EmbeddingWorker

---

# Technology Stack

## Backend

- Python 3.12
- FastAPI
- SQLAlchemy Async
- PostgreSQL
- Alembic
- Pydantic v2

## Frontend

- React
- TypeScript
- Material UI

## AI

### Current

- LangChain Text Splitters

### Planned

- Sentence Transformers
- Ollama
- OpenAI
- ChromaDB

---

# Supported Document Formats

Currently supported

- PDF
- DOCX
- TXT
- HTML
- Markdown

Future

- OCR
- Images
- Excel
- PowerPoint

---

# Project Structure

```text
knowledge-assistant/

├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── commands/
│   │   ├── core/
│   │   ├── models/
│   │   ├── providers/
│   │   │   ├── parser/
│   │   │   ├── chunker/
│   │   │   └── embedding/
│   │   ├── repositories/
│   │   ├── services/
│   │   ├── workers/
│   │   └── schemas/
│   ├── migrations/
│   ├── storage/
│   └── tests/
│
├── frontend/
├── docs/
├── scripts/
└── README.md
```

---

# Design Principles

The project follows these architectural principles.

- Clean Architecture
- SOLID Principles
- CQRS
- Repository Pattern
- ExecutionContext
- Workflow Services
- Provider Services
- Factory Pattern
- Background Workers
- Async First
- Strong Typing
- Single Responsibility Principle

---

# API Response

Every endpoint returns a consistent response.

```json
{
  "code": "SUCCESS",
  "success": true,
  "message": "Operation completed successfully.",
  "result": {},
  "total_records": null,
  "request_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
}
```

---

# Current API

## Health

```http
GET /api/v1/health
```

---

## Upload Document

```http
POST /api/v1/documents/upload
```

Supported document types

- PDF
- DOCX
- TXT
- HTML
- Markdown

---

# Documentation

Additional documentation is available in the `docs/` directory.

- architecture.md
- roadmap.md
- rag-pipeline.md
- decisions.md
- api.md
- setup.md

---

# Roadmap

| Milestone           | Status  |
| ------------------- | ------- |
| Backend Foundation  | ✅      |
| Document Processing | ✅      |
| Document Chunking   | ✅      |
| Embeddings          | 🚧      |
| Vector Database     | Planned |
| Semantic Search     | Planned |
| AI Chat             | Planned |
| Enterprise Features | Planned |

---

# License

MIT License

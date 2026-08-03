# Knowledge Assistant

An enterprise-grade, provider-agnostic Knowledge Assistant built with **FastAPI**, **React**, and a modular **Retrieval-Augmented Generation (RAG)** architecture.

The platform enables organizations to upload documents, build an intelligent knowledge base, perform semantic search, and generate grounded AI responses using their own data.

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
- Supports multiple Large Language Models (LLMs)
- Remains modular and provider independent

The architecture follows **Clean Architecture** principles, where every processing stage has a single responsibility and can evolve independently.

---

# Current Status

## ✅ Completed

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

### Document Embeddings

- Embedding Provider Architecture
- Embedding Factory
- Sentence Transformer Provider
- Document Embedder Service
- Background Embedding Worker
- PostgreSQL pgvector Integration
- Vector Embedding Persistence
- End-to-End Embedding Pipeline

---

## 🚧 In Progress

- Vector Similarity Search
- Query Embeddings
- Semantic Retrieval

---

## Planned

- Prompt Builder
- AI Chat
- Conversation History
- Authentication
- Multi-Tenant Support
- Monitoring
- CI/CD

---

# Processing Pipeline

The backend currently implements the following document ingestion pipeline.

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
Generate Embeddings
        │
        ▼
Store in PostgreSQL (pgvector)
        │
        ▼
Semantic Retrieval (Next)
        │
        ▼
Prompt Builder
        │
        ▼
Large Language Model
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
          ┌──────────────┴──────────────┐
          ▼                             ▼
  Provider Service               Repository
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
        │
        ▼
Worker
        │
        ▼
ExecutionContext
        │
        ▼
Command
        │
        ▼
Workflow Service
        │
        ▼
Provider Service
        │
        ▼
Repository
```

### Current Workers

- DocumentWorker
- ChunkWorker
- EmbeddingWorker

Each worker processes documents independently, providing isolated transactions and failure recovery.

---

# Technology Stack

## Backend

- Python 3.12
- FastAPI
- SQLAlchemy Async
- PostgreSQL 18
- pgvector
- Alembic
- Pydantic v2

## Frontend

- React
- TypeScript
- Material UI

## AI

### Current

- LangChain Text Splitters
- Sentence Transformers (`all-MiniLM-L6-v2`)
- PostgreSQL + pgvector

### Planned

- Ollama
- OpenAI
- Anthropic
- Gemini

---

# Supported Document Formats

### Current

- PDF
- DOCX
- TXT
- HTML
- Markdown

### Future

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
│   │   ├── dtos/
│   │   ├── models/
│   │   ├── providers/
│   │   │   ├── parsers/
│   │   │   ├── chunkers/
│   │   │   └── embeddings/
│   │   ├── queries/
│   │   ├── repositories/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── workers/
│   │   └── utils/
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

Returns application health information.

---

## Upload Document

```http
POST /api/v1/documents/upload
```

Supported document types:

- PDF
- DOCX
- TXT
- HTML
- Markdown

---

# Documentation

Additional documentation is available in the `docs/` directory.

- `architecture.md`
- `roadmap.md`
- `rag-pipeline.md`
- `decisions.md`
- `api.md`
- `setup.md`

---

# Roadmap

| Phase                | Status         |
| -------------------- | -------------- |
| Backend Foundation   | ✅ Completed   |
| Document Processing  | ✅ Completed   |
| Document Chunking    | ✅ Completed   |
| Document Embeddings  | ✅ Completed   |
| Vector Search        | 🚧 In Progress |
| AI Chat              | Planned        |
| Enterprise Features  | Planned        |
| Production Readiness | Planned        |

---

# License

MIT License

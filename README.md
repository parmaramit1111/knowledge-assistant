# Knowledge Assistant

A provider-agnostic Knowledge Assistant built with **FastAPI**, **React**, and a modular **Retrieval-Augmented Generation (RAG)** architecture.

The platform enables users to upload documents, build an intelligent knowledge base, perform semantic search, retrieve relevant context, and generate grounded AI responses using their own data.

---

# Vision

The goal of this project is to demonstrate a clean, modular, provider-agnostic RAG architecture that showcases:

- Multiple document formats
- Document parsing
- Document chunking
- Vector embeddings
- Semantic similarity search
- Context retrieval
- Grounded AI responses
- Provider abstraction
- Prompt provider architecture
- LLM provider architecture
- Vector database integration
- Clean Architecture principles
- Full-stack integration

Every processing stage has a single responsibility and can evolve independently.

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
- CORS Configuration

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
- Optimized Chunking (800 / 200)
- Custom Chunk Separators
- Document Chunk Persistence
- Background Chunk Worker

### Document Embeddings

- Embedding Provider Architecture
- Embedding Factory
- Sentence Transformer Provider
- Document Embedder Service
- Query Embedder Service
- Background Embedding Worker
- PostgreSQL pgvector Integration
- Vector Embedding Persistence
- End-to-End Embedding Pipeline

### Semantic Search

- Search API
- Query Embedding Pipeline
- PGVector Cosine Similarity Search
- Ranked Search Results
- Document Metadata Retrieval
- End-to-End Semantic Retrieval Pipeline

### AI Chat (RAG)

- Chat API
- Ask Question Command
- Document Chat Service
- Prompt Builder Service
- Prompt Provider Architecture
- Prompt Factory
- Default Prompt Provider
- LLM Provider Architecture
- LLM Factory
- Ollama Provider
- Prompt Generation
- Context Injection
- Grounded AI Responses
- Source Document References
- End-to-End RAG Chat Pipeline

### Frontend

- React
- TypeScript
- Vite
- Material UI
- Chat Interface
- Chat API Integration
- Conversation State Management
- Source References
- PDF Document Upload
- Drag & Drop Upload
- Upload Status Handling
- Upload Success/Error Handling
- New Chat
- Sidebar Navigation
- Collapsible Sidebar
- Responsive Chat Layout
- Application Theme
- Knowledge Assistant Branding

---

# Processing Pipeline

The Knowledge Assistant implements the following Retrieval-Augmented Generation pipeline.

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
Semantic Search
        │
        ▼
Prompt Builder
        │
        ▼
Large Language Model
        │
        ▼
Grounded AI Response
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
          │                             │
          ▼                             ▼
    Provider Factory               PostgreSQL
          │
          ▼
        Provider
```

---

# Background Processing

Long-running document processing operations execute asynchronously.

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
Provider
        │
        ▼
Repository
```

### Current Workers

- DocumentWorker
- ChunkWorker
- EmbeddingWorker

Each worker processes documents independently using its own execution context and transaction boundary.

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
- Vite
- Material UI

## AI

- LangChain Recursive Character Text Splitter
- Sentence Transformers (`all-MiniLM-L6-v2`)
- PostgreSQL + pgvector
- Semantic Vector Search
- Ollama
- Prompt Provider Architecture
- LLM Provider Architecture

---

# Supported Document Formats

- PDF
- DOCX
- TXT
- HTML
- Markdown

The parser architecture allows additional document formats to be introduced without changing the core processing workflow.

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
│   │   │   ├── embeddings/
│   │   │   ├── prompts/
│   │   │   └── llm/
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
│   ├── public/
│   └── src/
│       ├── api/
│       ├── components/
│       ├── hooks/
│       ├── pages/
│       └── ...
│
├── docs/
├── scripts/
└── README.md
```

---

# Design Principles

The project follows these architectural principles:

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
- Provider Independence

---

# Current API

## Health

```http
GET /api/v1/health
```

## Upload Document

```http
POST /api/v1/documents/upload
```

## Semantic Search

```http
POST /api/v1/search
```

## AI Chat

```http
POST /api/v1/chat
```

Returns a grounded AI response using retrieved document context.

---

# Documentation

Additional documentation is available in the `docs/` directory.

- `architecture.md`
- `roadmap.md`
- `rag-pipeline.md`
- `decisions.md`
- `api.md`
- `setup.md`
- `deployment.md`

---

# Project Scope

The project focuses on demonstrating the core engineering capabilities required to design and implement a modern RAG application:

- Document ingestion
- Document processing
- Document chunking
- Embedding generation
- Vector storage
- Semantic retrieval
- Prompt construction
- LLM integration
- Grounded responses
- Source attribution
- Provider-independent architecture
- Background processing
- Clean backend architecture
- Full-stack React integration
- Document upload experience
- Chat interface
- Technical documentation

The project is intentionally maintained as a **RAG engineering showcase and reference implementation**, rather than being extended into a production SaaS platform.

---

# Project Completion

The core showcase implementation is complete.

```text
Backend Foundation        ✅
Document Processing       ✅
Document Chunking         ✅
Embedding Pipeline        ✅
Semantic Search           ✅
Prompt Builder            ✅
AI Chat (RAG)             ✅
Frontend Experience       ✅
Technical Documentation   ✅
```

The architecture can serve as the foundation for a separate private production RAG implementation when production infrastructure and operational requirements are needed.

---

# License

MIT License

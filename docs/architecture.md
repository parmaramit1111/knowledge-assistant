# Backend Architecture

## Overview

The Knowledge Assistant backend is designed as a modular application following **Clean Architecture** principles.

The architecture separates business workflow, provider integrations, persistence, and infrastructure into well-defined layers to maximize maintainability, scalability, and extensibility.

The backend is built around the following architectural patterns:

- Clean Architecture
- CQRS
- Repository Pattern
- ExecutionContext
- Workflow Services
- Provider Services
- Factory Pattern
- Background Workers
- Async First Design
- Provider Independence

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

### Cross-cutting Concerns

- Transactions
- Logging
- Exception Handling
- Configuration
- Dependency Management
- Request Correlation ID
- CORS

---

# Design Principles

The backend follows these principles:

- Clean Architecture
- SOLID Principles
- CQRS
- Repository Pattern
- ExecutionContext
- Workflow Services
- Provider Services
- Factory Pattern
- Strong Typing
- Async First
- Single Responsibility Principle
- Provider Independence

The core business workflow remains independent of concrete infrastructure and provider implementations.

---

# Project Structure

```text
backend/
│
├── app/
│   ├── api/
│   ├── commands/
│   ├── core/
│   ├── dtos/
│   ├── models/
│   ├── providers/
│   │   ├── parsers/
│   │   ├── chunkers/
│   │   ├── embeddings/
│   │   ├── prompts/
│   │   └── llm/
│   ├── queries/
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   ├── workers/
│   └── utils/
│
├── migrations/
├── storage/
└── tests/
```

---

# Layer Responsibilities

## API Layer

**Location**

```text
app/api/
```

### Responsibilities

- Define REST endpoints
- Validate requests
- Return standardized responses
- Execute Commands or Queries
- Handle HTTP-specific concerns

Controllers never contain business logic.

---

## ExecutionContext

**Location**

```text
app/core/execution/
```

ExecutionContext manages the lifecycle of an HTTP request or background task by creating repositories, services, and a database session for each execution scope.

It provides a consistent execution boundary for both synchronous API operations and background processing.

---

## Commands

**Location**

```text
app/commands/
```

### Current Commands

- UploadDocumentCommand
- ParseDocumentCommand
- ChunkDocumentCommand
- EmbedDocumentCommand
- SearchDocumentsCommand
- AskQuestionCommand

Commands coordinate business workflows and never contain persistence logic.

---

## Queries

**Location**

```text
app/queries/
```

### Current Queries

- GetDocumentQuery
- HealthCheckQuery

Queries execute read operations without modifying application state.

---

# Services

The application separates services into two categories.

---

## Workflow Services

### Current Services

- DocumentWorkflowService
- DocumentProcessingService
- DocumentChunkingService
- DocumentEmbeddingService
- DocumentSearchService
- DocumentChatService

Workflow services orchestrate business processes and coordinate repositories and provider services.

---

## Provider Services

### Current Services

- DocumentParserService
- DocumentChunkerService
- DocumentEmbedderService
- QueryEmbedderService
- PromptBuilderService
- LLMService

Provider services encapsulate provider-specific execution and transformations and never perform persistence.

---

# Providers

**Location**

```text
app/providers/
```

## Current Providers

### Document Parsers

- PDF Parser
- Word Parser
- HTML Parser
- Markdown Parser
- Text Parser

### Chunkers

- Recursive Character Splitter

### Embeddings

- Sentence Transformers (`all-MiniLM-L6-v2`)

### Prompts

- Default Prompt Provider

### Large Language Models

- Ollama (`qwen2.5:1.5b`)

---

# Future Provider Options

The provider architecture allows additional implementations to be introduced without changing the core business workflow.

### Embeddings

- Ollama Embeddings
- OpenAI Embeddings

### Prompts

- Technical Support Prompt
- FAQ Prompt
- Customer Support Prompt
- Custom Prompt Templates

### LLMs

- OpenAI
- Anthropic
- Gemini
- Azure OpenAI

Providers contain integration logic only.

---

# Provider Factories

Factories select the appropriate provider implementation.

```text
ParserFactory
        │
        ▼
PDF
DOCX
TXT
HTML
Markdown
```

```text
ChunkerFactory
        │
        ▼
RecursiveChunker
```

```text
EmbeddingFactory
        │
        ▼
SentenceTransformer
OpenAI (Future)
Ollama (Future)
```

```text
PromptFactory
        │
        ▼
DefaultPrompt
CustomPrompt (Future)
```

```text
LLMFactory
        │
        ▼
Ollama
OpenAI (Future)
Anthropic (Future)
Gemini (Future)
```

Business workflows never depend directly on concrete provider implementations.

---

# Repositories

**Location**

```text
app/repositories/
```

### Responsibilities

- CRUD operations
- Persistence
- Search
- Vector Similarity Search
- Database Queries

Repositories remain responsible only for data access and never contain business logic.

---

# Models

**Location**

```text
app/models/
```

Models represent persistence entities and are never exposed directly through the API.

---

# Schemas

**Location**

```text
app/schemas/
```

Schemas define public API contracts and remain independent from persistence models.

---

# Request Lifecycle

```text
Client
    │
    ▼
Controller
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
    ├───────────────┐
    ▼               ▼
Provider Service  Repository
    │               │
    ▼               ▼
 Provider        Database
    │               │
    └───────┬───────┘
            ▼
       API Response
```

---

# Chat Request Lifecycle

```text
User Question
      │
      ▼
Chat Controller
      │
      ▼
AskQuestionCommand
      │
      ▼
DocumentChatService
      │
      ├────────► DocumentSearchService
      │               │
      │               ▼
      │         Query Embedder
      │               │
      │               ▼
      │         Semantic Search
      │
      ├────────► PromptBuilderService
      │               │
      │               ▼
      │         PromptFactory
      │               │
      │               ▼
      │        DefaultPrompt
      │
      └────────► LLMService
                      │
                      ▼
                 LLMFactory
                      │
                      ▼
               OllamaProvider
                      │
                      ▼
                 Grounded Response
                      │
                      ▼
                Source References
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

Each worker processes documents independently using its own ExecutionContext and transaction.

---

# Database

### Database

- PostgreSQL 18

### Extensions

- pgvector

### ORM

- SQLAlchemy Async

### Migration

- Alembic

### Features

- UUID Primary Keys
- Async Queries
- Connection Pooling
- Vector Embeddings
- Cosine Similarity Search
- Transactional Processing

---

# Current Processing Pipeline

```text
Upload
    │
    ▼
Parse
    │
    ▼
Chunk
    │
    ▼
Embed
    │
    ▼
PostgreSQL (pgvector)
    │
    ▼
Semantic Search
    │
    ▼
Prompt Builder
    │
    ▼
LLM Provider
    │
    ▼
Grounded AI Response
```

---

# Frontend Integration

The React frontend communicates with the backend through a dedicated API layer.

```text
React UI
    │
    ▼
Custom Hook
    │
    ▼
API Service
    │
    ▼
FastAPI
    │
    ▼
Application Services
```

### Current Frontend Integrations

```text
Chat UI
    │
    ▼
useChat
    │
    ▼
Chat API
    │
    ▼
POST /api/v1/chat
```

```text
Document Upload UI
    │
    ▼
useDocumentUpload
    │
    ▼
Document API
    │
    ▼
POST /api/v1/documents/upload
```

CORS is configured on the backend to allow browser-based communication with the frontend during development and deployment.

---

# Provider Independence

### Parsers

- PDF
- DOCX
- TXT
- HTML
- Markdown

### Chunkers

- Recursive Character Splitter
- Semantic Splitter (Future)

### Embeddings

- Sentence Transformers
- Ollama (Future)
- OpenAI (Future)

### Prompts

- Default Prompt
- Custom Prompt (Future)

### Vector Databases

- PostgreSQL (pgvector)
- ChromaDB (Future)
- Milvus (Future)
- Qdrant (Future)

### Large Language Models

- Ollama
- OpenAI (Future)
- Anthropic (Future)
- Gemini (Future)
- Azure OpenAI (Future)

Adding a new provider should require changes only within the provider abstraction and configuration layers without changing the core business workflows.

---

# Production Readiness

The core backend RAG pipeline and frontend experience are complete.

The next phase focuses on deployment and production readiness.

### Next

- Docker
- Docker Compose
- Backend Containerization
- Frontend Containerization
- PostgreSQL Configuration
- Environment Management
- Production Configuration
- Deployment Configuration
- Reverse Proxy
- CI/CD
- Unit Tests
- Integration Tests
- Monitoring
- Metrics
- Health Checks
- Rate Limiting
- Prompt & LLM Performance Metrics
- Performance Validation

---

# Engineering Goals

The architecture is designed to remain:

- Modular
- Extensible
- Provider Independent
- Testable
- Maintainable
- Cloud Ready
- AI Ready
- Deployment Ready

The project intentionally focuses on demonstrating strong **RAG engineering, clean architecture, provider independence, full-stack integration, and production deployment practices** without coupling the core application to a specific infrastructure provider.

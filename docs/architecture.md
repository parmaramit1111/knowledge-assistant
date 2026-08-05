# Backend Architecture

## Overview

The Knowledge Assistant backend is designed as a modular, enterprise-grade application following **Clean Architecture** principles.

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

---

# Design Principles

The backend follows these principles.

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

---

# Project Structure

```text
backend/
│
├── app/
│   │
│   ├── api/
│   ├── commands/
│   ├── core/
│   ├── dtos/
│   ├── models/
│   ├── providers/
│   │   ├── parsers/
│   │   ├── chunkers/
│   │   └── embeddings/
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

```
app/api/
```

### Responsibilities

- Define REST endpoints
- Validate requests
- Return standardized responses
- Execute Commands or Queries

Controllers never contain business logic.

---

## ExecutionContext

**Location**

```
app/core/execution/
```

ExecutionContext manages the lifecycle of an HTTP request or background task by creating repositories, services and a database session for each execution scope.

---

## Commands

**Location**

```
app/commands/
```

### Examples

- UploadDocumentCommand
- ParseDocumentCommand
- ChunkDocumentCommand
- EmbedDocumentCommand

Commands execute write operations and coordinate business workflows.

---

## Queries

**Location**

```
app/queries/
```

### Examples

- GetDocumentQuery
- SearchDocumentsQuery
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
- **DocumentSearchService**

Workflow services orchestrate business processes and coordinate repositories and provider services.

---

## Provider Services

### Current Services

- DocumentParserService
- DocumentChunkerService
- DocumentEmbedderService
- **QueryEmbedderService**

Provider services encapsulate provider-specific logic and never perform persistence.

---

# Providers

**Location**

```
app/providers/
```

### Current Providers

#### Document Parsers

- PDF Parser
- Word Parser
- HTML Parser
- Markdown Parser
- Text Parser

#### Chunkers

- Recursive Character Splitter

#### Embeddings

- Sentence Transformers (`all-MiniLM-L6-v2`)

### Future Providers

- Ollama Embeddings
- OpenAI Embeddings
- Additional Embedding Providers

Providers contain integration logic only.

---

# Provider Factories

Factories select the appropriate provider implementation.

```text
ParserFactory

↓

PDF Parser
Word Parser
HTML Parser
Markdown Parser
Text Parser
```

```text
ChunkerFactory

↓

RecursiveChunker
```

```text
EmbeddingFactory

↓

SentenceTransformerEmbedding
OpenAIEmbedding (Future)
OllamaEmbedding (Future)
```

Business workflow never depends on a concrete provider implementation.

---

# Repositories

**Location**

```
app/repositories/
```

### Current Responsibilities

- CRUD operations
- Search
- Persistence
- Vector Similarity Search
- Database Queries

Repositories remain responsible only for data access and never contain business logic.

---

# Models

**Location**

```
app/models/
```

Models represent persistence entities and are never exposed directly through the API.

---

# Schemas

**Location**

```
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
    ▼
Provider Service
    │
    ▼
Repository
    │
    ▼
Commit / Response
```

---

# Background Processing

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

Each worker processes documents independently using its own ExecutionContext and transaction.

---

# Transaction Management

Every Command executes inside an ambient transaction managed by ExecutionContext.

---

# Dependency Management

```text
ExecutionContext
        │
        ▼
Repositories
        │
        ▼
Workflow Services
        │
        ▼
Provider Services
        │
        ▼
Commands / Queries
```

ExecutionContext serves as the application's dependency container.

---

# CQRS

### Commands

- Upload
- Parse
- Chunk
- Embed

### Queries

- Search
- Read
- Retrieve

---

# Exception Handling

Global exception handlers convert exceptions into standardized API responses while background workers log failures without interrupting pipeline execution.

---

# Standard API Response

Every endpoint returns

```json
{
  "code": "SUCCESS",
  "success": true,
  "message": "...",
  "result": {},
  "total_records": null,
  "request_id": "..."
}
```

---

# Database

### Database

- PostgreSQL 18

### Extensions

- pgvector

### ORM

- SQLAlchemy Async

### Features

- UUID Primary Keys
- Async Queries
- Connection Pooling
- Vector Embeddings
- Cosine Similarity Search

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
LLM
    │
    ▼
Grounded Response
```

---

# Provider Independence

### Document Parsers

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
- Ollama
- OpenAI

### Vector Databases

- PostgreSQL (pgvector)
- ChromaDB
- Milvus
- Qdrant

### Large Language Models

- Ollama
- OpenAI
- Anthropic
- Gemini

Adding a new provider should require no changes to business workflow.

---

# Engineering Goals

The architecture is designed to remain:

- Modular
- Extensible
- Provider Independent
- Testable
- Maintainable
- Enterprise Ready
- Cloud Ready
- AI Ready

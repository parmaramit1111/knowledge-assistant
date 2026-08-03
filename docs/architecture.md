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

### Purpose

ExecutionContext manages the lifecycle of an HTTP request or background task.

### Responsibilities

- Create database session
- Create repositories
- Create workflow services
- Create provider services
- Dispose resources
- Share dependencies across Commands and Queries

ExecutionContext acts as the application's dependency container.

---

## Commands

**Location**

```
app/commands/
```

### Purpose

Commands represent write operations.

### Examples

- UploadDocumentCommand
- ParseDocumentCommand
- ChunkDocumentCommand
- EmbedDocumentCommand

### Responsibilities

- Receive validated input
- Execute application use cases
- Coordinate workflow through services

Commands never access repositories directly.

---

## Queries

**Location**

```
app/queries/
```

### Purpose

Queries represent read operations.

### Examples

- GetDocumentQuery
- SearchDocumentsQuery
- HealthCheckQuery

Queries never modify application state.

---

# Services

The application separates services into two categories.

---

## Workflow Services

### Purpose

Workflow services orchestrate business processes.

### Examples

- DocumentWorkflowService
- DocumentProcessingService
- DocumentChunkingService
- DocumentEmbeddingService

### Responsibilities

- Business workflow
- State transitions
- Repository coordination
- Background processing
- Error handling

Workflow services own the application workflow.

---

## Provider Services

### Purpose

Provider services perform business transformations using external providers.

### Examples

- DocumentParserService
- DocumentChunkerService
- DocumentEmbedderService

### Responsibilities

- Select providers
- Execute providers
- Transform domain models

Provider services never perform persistence or workflow management.

---

# Providers

**Location**

```
app/providers/
```

### Purpose

Providers integrate external libraries and technologies.

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
- Additional embedding providers

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
(OpenAI, Ollama - Future)
```

Business workflow never depends on a concrete provider implementation.

---

# Repositories

**Location**

```
app/repositories/
```

### Responsibilities

- CRUD operations
- Search
- Persistence
- Database queries

Every repository inherits from the generic `BaseRepository`.

Shared functionality includes:

- add()
- add_many()
- update()
- delete()
- get_by_id()
- find()
- find_one()
- exists()
- count()

Repositories never contain business logic.

---

# Models

**Location**

```
app/models/
```

### Responsibilities

- SQLAlchemy entity mapping
- Relationships
- Constraints
- Persistence

Models are never exposed directly through the API.

---

# Schemas

**Location**

```
app/schemas/
```

### Responsibilities

- Request Models
- Response Models
- API Contracts

Schemas remain independent from persistence models.

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
    │
    ▼
Commit / Rollback
    │
    ▼
API Response
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

Each document is processed inside its own ExecutionContext, providing isolated transactions and failure recovery.

---

# Transaction Management

Every Command executes inside an ambient transaction.

```text
ExecutionContext
    │
    ▼
Create AsyncSession
    │
    ▼
Execute Command
    │
    ▼
Workflow Service
    │
    ▼
Repository
    │
    ▼
Commit / Rollback
    │
    ▼
Dispose Session
```

---

# Dependency Management

Dependencies are centrally managed through ExecutionContext.

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

This eliminates the need for external dependency injection frameworks.

---

# CQRS

The application separates write and read operations.

### Commands

- Create
- Update
- Delete
- Background Processing

### Queries

- Read
- Search
- Retrieve

Benefits:

- Clear responsibility separation
- Easier testing
- Better scalability

---

# Exception Handling

Global exception handlers convert exceptions into standardized API responses.

```text
ValidationException
        │
        ▼
HTTP 400
```

```text
NotFoundException
        │
        ▼
HTTP 404
```

```text
Unhandled Exception
        │
        ▼
HTTP 500
```

Background workers log failures while preserving workflow state.

---

# Standard API Response

Every endpoint returns:

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

### Migration

- Alembic

### Features

- UUID Primary Keys
- Async Queries
- Connection Pooling
- Transaction Management
- Vector Embeddings

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
Generate Embeddings
    │
    ▼
PostgreSQL (pgvector)
    │
    ▼
Semantic Retrieval (Next)
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

The architecture is provider-agnostic.

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

Adding a new provider should require no changes to the application workflow.

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

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

Cross-cutting concerns

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
│   ├── models/
│   ├── providers/
│   │   ├── parser/
│   │   ├── chunker/
│   │   └── embedding/
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

Location

```
app/api/
```

Responsibilities

- Define REST endpoints
- Validate requests
- Return standardized responses
- Execute Commands or Queries

Controllers never contain business logic.

---

## ExecutionContext

Location

```
app/core/execution/
```

Purpose

ExecutionContext manages the lifecycle of a request or background operation.

Responsibilities

- Create database session
- Create repositories
- Create services
- Dispose resources
- Share dependencies through Commands

ExecutionContext acts as the application's Dependency Injection container.

---

## Commands

Location

```
app/commands/
```

Purpose

Commands represent write operations.

Examples

- UploadDocumentCommand
- ParseDocumentCommand
- ChunkDocumentCommand

Responsibilities

- Receive validated input
- Execute application use cases
- Coordinate workflow through services

Commands never access repositories directly.

---

## Queries

Location

```
app/queries/
```

Purpose

Queries represent read operations.

Examples

- GetDocumentQuery
- SearchDocumentsQuery
- HealthCheckQuery

Queries never modify data.

---

# Services

The application separates services into two categories.

---

## Workflow Services

Purpose

Workflow services orchestrate business processes.

Examples

- DocumentWorkflowService
- DocumentProcessingService
- DocumentChunkingService

Responsibilities

- Business workflow
- State transitions
- Repository coordination
- Background processing
- Error handling

Workflow services own the application workflow.

---

## Provider Services

Purpose

Provider services perform business transformations.

Examples

- DocumentParserService
- DocumentChunkerService

Responsibilities

- Select providers
- Execute providers
- Transform domain models

Provider services never perform persistence or workflow management.

---

# Providers

Location

```
app/providers/
```

Purpose

Providers integrate external libraries and technologies.

Examples

Document Parsers

- PDF Parser
- Word Parser
- HTML Parser
- Markdown Parser
- Text Parser

Chunkers

- Recursive Character Splitter

Future Providers

- OpenAI Embeddings
- Sentence Transformers
- Ollama Embeddings

Providers contain integration logic only.

---

# Provider Factories

Factories select the appropriate provider.

Example

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

Future

```text
EmbeddingFactory

↓

OpenAI
Sentence Transformers
Ollama
```

Business logic never depends on a specific provider implementation.

---

# Repositories

Location

```
app/repositories/
```

Purpose

Repositories provide persistence.

Responsibilities

- CRUD
- Search
- Persistence
- Database Queries

Repositories never contain business logic.

Every repository inherits from the generic BaseRepository.

Shared functionality

- add()
- add_many()
- update()
- delete()
- get_by_id()
- find()
- find_one()
- exists()
- count()

---

# Models

Location

```
app/models/
```

Purpose

Database entities mapped through SQLAlchemy.

Responsibilities

- Persistence mapping
- Relationships
- Database constraints

Models are never returned directly by the API.

---

# Schemas

Location

```
app/schemas/
```

Purpose

Public API contracts.

Contains

- Request Models
- Response Models
- DTOs
- ApiResponse

Schemas remain independent of persistence models.

---

# Request Lifecycle

```text
Client

↓

Controller

↓

ExecutionContext

↓

Command

↓

Workflow Service

↓

Provider Service

↓

Provider

↓

Repository

↓

Commit / Rollback

↓

API Response
```

---

# Background Processing

The application processes long-running operations asynchronously.

Architecture

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

Current Workers

- DocumentWorker
- ChunkWorker

Future Workers

- EmbeddingWorker

Each document is processed inside its own ExecutionContext, providing independent transactions and failure isolation.

---

# Transaction Management

Every Command executes inside a transaction.

Transaction lifecycle

```text
ExecutionContext

↓

Create AsyncSession

↓

Execute Command

↓

Workflow Service

↓

Repository

↓

Commit

or

Rollback

↓

Dispose Session
```

Each background task receives an isolated transaction.

---

# Dependency Management

Dependencies are managed through ExecutionContext.

```text
ExecutionContext

↓

Repositories

↓

Workflow Services

↓

Provider Services

↓

Commands
```

This centralizes dependency creation and eliminates service factories.

---

# CQRS

The application separates reads from writes.

Commands

- Create
- Update
- Delete
- Background Processing

Queries

- Search
- Read
- Retrieve

Benefits

- Clear separation of responsibilities
- Easier testing
- Better scalability

---

# Exception Handling

Global exception handlers convert exceptions into standardized API responses.

```text
ValidationException

↓

HTTP 400
```

```text
NotFoundException

↓

HTTP 404
```

```text
Unhandled Exception

↓

HTTP 500
```

Background workers log failures while maintaining workflow state.

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

Database

- PostgreSQL

ORM

- SQLAlchemy Async

Migration

- Alembic

Features

- UUID Primary Keys
- Async Queries
- Connection Pooling
- Transaction Management

---

# Processing Pipeline

The current document processing pipeline is

```text
Upload

↓

Parse

↓

Chunk

↓

Embeddings (Upcoming)

↓

Vector Database

↓

Retrieval

↓

Prompt Builder

↓

LLM

↓

Response
```

---

# Provider Independence

The architecture is provider-agnostic.

Document Parsers

- PDF
- DOCX
- TXT
- HTML
- Markdown

Chunkers

- Recursive Character Splitter
- Semantic Splitter (Future)

Embeddings

- Sentence Transformers
- Ollama
- OpenAI

Vector Databases

- ChromaDB
- PGVector
- Milvus
- Qdrant

LLMs

- Ollama
- OpenAI
- Anthropic
- Gemini

Adding a new provider should require no changes to business workflow.

---

# Engineering Goals

The architecture is designed to remain

- Modular
- Extensible
- Provider Independent
- Testable
- Maintainable
- Enterprise Ready
- Cloud Ready
- AI Ready

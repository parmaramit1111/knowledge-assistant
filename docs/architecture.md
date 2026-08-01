# Backend Architecture

## Overview

The Knowledge Assistant backend is designed as a modular, enterprise-grade application built on **Clean Architecture** principles.

The primary goals of the architecture are:

- Separation of Concerns
- Maintainability
- Scalability
- Testability
- Extensibility
- Provider Independence

The application follows a layered architecture combined with **CQRS**, **Repository Pattern**, **Ambient Transactions**, and **Dependency Factories**.

---

# Architecture Overview

```text
                HTTP Request
                     │
                     ▼
             FastAPI Controller
                     │
                     ▼
              Command / Query
                     │
                     ▼
                  Service
                     │
                     ▼
                Repository
                     │
                     ▼
                 PostgreSQL
```

Cross-cutting concerns:

- Transactions
- Logging
- Exception Handling
- Request Context
- Response Formatting

---

# Design Principles

The backend follows these principles.

- Clean Architecture
- SOLID Principles
- CQRS
- Repository Pattern
- Ambient Transactions
- Provider Pattern
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
│   ├── queries/
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   └── utils/
│
├── migrations/
├── storage/
└── tests/
```

---

# Layer Responsibilities

---

## API Layer

Location

```
app/api/
```

Responsibilities

- Define REST endpoints
- Validate HTTP requests
- Return standardized responses
- Execute Commands or Queries

Controllers never contain business logic.

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
- DeleteDocumentCommand
- UpdateDocumentCommand

Responsibilities

- Receive validated input
- Execute inside a transaction
- Call the appropriate service

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

- HealthCheckQuery
- GetDocumentQuery
- SearchDocumentsQuery

Queries never modify data.

---

## Services

Location

```
app/services/
```

Purpose

Business logic lives here.

Responsibilities

- Validation
- Orchestration
- Domain rules
- DTO ↔ Entity mapping

Services coordinate repositories and providers.

---

## Repositories

Location

```
app/repositories/
```

Purpose

Repositories provide database access.

Responsibilities

- CRUD
- Queries
- Persistence

Repositories contain no business logic.

Repositories automatically use the active transaction through the transaction context.

---

## Models

Location

```
app/models/
```

Purpose

SQLAlchemy ORM models.

Responsibilities

- Database mapping
- Relationships
- Persistence model

Models should not be returned directly to API clients.

---

## Schemas

Location

```
app/schemas/
```

Purpose

Public API contracts.

Contains

- Request Models
- Response Models
- Shared DTOs
- ApiResponse

Schemas are independent of the database.

---

## Providers

Location

```
app/providers/
```

Purpose

Integrate with external systems.

Examples

- PDF Parser
- ChromaDB
- Ollama
- OpenAI
- Sentence Transformers

Providers contain integration logic only.

---

## Core

Location

```
app/core/
```

Purpose

Infrastructure shared by the application.

Contains

- Configuration
- Database
- Middleware
- Transactions
- Exception Handling
- Dependencies
- Logging
- Security

---

# Request Lifecycle

```text
Client

↓

Controller

↓

Command

↓

@transactional

↓

Service

↓

Repository

↓

Database

↓

Commit / Rollback

↓

API Response
```

---

# Transaction Management

The application uses Ambient Transactions.

Transaction lifecycle

```text
Command

↓

@transactional

↓

Create AsyncSession

↓

Store Session in ContextVar

↓

Execute Service

↓

Repository retrieves Session

↓

Commit

or

Rollback

↓

Dispose Session
```

Repositories never receive the session explicitly.

Instead they retrieve the active session from the transaction context.

Benefits

- Cleaner service code
- No session plumbing
- Automatic Unit of Work

---

# Dependency Management

Dependencies are created through factories.

```text
ServiceFactory

↓

DocumentUploadService
```

```text
RepositoryFactory

↓

DocumentRepository
```

This keeps object creation centralized.

---

# Repository Pattern

Every repository inherits from the generic BaseRepository.

Example

```text
BaseRepository

↓

DocumentRepository

↓

Future Repositories
```

Shared functionality

- Add
- Update
- Delete
- GetById
- Exists
- Count

---

# CQRS

The application separates reads and writes.

Commands

- Create
- Update
- Delete

Queries

- Search
- Read
- Retrieve

Benefits

- Simpler code
- Better scalability
- Easier testing

---

# Exception Handling

Global exception handlers translate exceptions into consistent API responses.

```text
ValidationException

↓

Exception Handler

↓

HTTP 400
```

```text
NotFoundException

↓

Exception Handler

↓

HTTP 404
```

```text
InternalException

↓

Exception Handler

↓

HTTP 500
```

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

# Request Correlation

Every request receives a unique Request ID.

Flow

```text
HTTP Request

↓

RequestIdMiddleware

↓

ContextVar

↓

Logger

↓

Response Header
```

This makes troubleshooting much easier.

---

# Database

Database

- PostgreSQL

ORM

- SQLAlchemy Async

Migration

- Alembic

Features

- UUID Keys
- Connection Pooling
- Async Queries
- Ambient Transactions

---

# RAG Architecture

The backend prepares documents for the Retrieval-Augmented Generation pipeline.

```text
Upload

↓

Parse

↓

Chunk

↓

Embeddings

↓

Vector Store

↓

Semantic Search

↓

Prompt

↓

LLM

↓

Response
```

The RAG pipeline is documented separately in **rag-pipeline.md**.

---

# Future Architecture

The architecture is designed to support multiple providers.

Examples

Document Parser

- PDF
- DOCX
- TXT

Embedding Provider

- Sentence Transformers
- Ollama
- OpenAI

Vector Store

- ChromaDB
- PGVector
- Milvus
- Qdrant

LLM

- Ollama
- OpenAI
- Anthropic
- Gemini

Adding a new provider should not require changes to business logic.

---

# Engineering Goals

The architecture is designed to remain:

- Modular
- Provider Independent
- Easy to Test
- Easy to Extend
- Enterprise Ready
- Cloud Ready
- AI Ready

# Knowledge Assistant

An enterprise-grade AI-powered Knowledge Assistant built with **FastAPI**, **React**, and a modular **Retrieval-Augmented Generation (RAG)** architecture.

The platform enables organizations to upload documents, build an intelligent knowledge base, and ask natural language questions with AI-generated answers grounded in their own data.

---

# Vision

The goal of this project is to build a production-ready knowledge platform that:

- Stores organizational knowledge
- Supports multiple document formats
- Generates semantic embeddings
- Performs vector similarity search
- Produces grounded AI responses
- Supports multiple LLM providers
- Is provider-agnostic and extensible

The application is designed around clean architecture principles so every component can evolve independently.

---

# Current Status

## Backend Foundation

**Status:** ✅ Completed

Implemented:

- FastAPI REST API
- CQRS (Command / Query Separation)
- Generic Repository Pattern
- Ambient Transaction using ContextVar
- Transaction Decorator (`@transactional`)
- SQLAlchemy 2.0 Async ORM
- PostgreSQL
- Alembic Migrations
- Global Exception Handling
- Standard API Response
- Request Correlation ID
- Connection Pooling
- Local Document Storage
- Document Upload API
- Repository Integration
- Transaction Rollback Support

---

# Planned Features

- PDF Parsing
- DOCX Parsing
- TXT Parsing
- Intelligent Document Chunking
- Embedding Generation
- ChromaDB Integration
- Semantic Search
- AI Chat
- Conversation History
- Authentication
- Multi-user Workspace
- Role-based Authorization
- Multiple LLM Providers
- Multiple Vector Database Providers

---

# High-Level Architecture

```text
                +---------------------+
                |     React Client    |
                +----------+----------+
                           |
                           |
                    REST API (FastAPI)
                           |
                           |
                +----------+----------+
                |    API Controllers  |
                +----------+----------+
                           |
                 Commands / Queries
                           |
                           |
                +----------+----------+
                |      Services       |
                +----------+----------+
                           |
                     Repositories
                           |
                           |
                   PostgreSQL Database

                           |
                           |
                    Document Storage

                           |
                           ▼

                     RAG Processing
```

---

# Backend Architecture

The backend follows a layered architecture.

```text
HTTP Request
      │
      ▼
Controller
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
Database
```

Cross-cutting concerns:

- Transaction Management
- Exception Handling
- Request Context
- Logging
- Response Formatting

---

# Technology Stack

## Backend

- Python 3.12
- FastAPI
- SQLAlchemy 2.0
- Alembic
- PostgreSQL
- Pydantic v2

## Frontend

- React
- TypeScript
- Material UI

## AI

- Ollama
- ChromaDB
- Sentence Transformers

---

# Project Structure

```text
knowledge-assistant/
│
├── backend/
│   │
│   ├── app/
│   │   │
│   │   ├── api/
│   │   ├── commands/
│   │   ├── core/
│   │   │   ├── dependencies/
│   │   │   ├── exceptions/
│   │   │   ├── handlers/
│   │   │   ├── middleware/
│   │   │   └── transaction/
│   │   │
│   │   ├── models/
│   │   ├── providers/
│   │   ├── queries/
│   │   ├── repositories/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── utils/
│   │
│   ├── migrations/
│   ├── storage/
│   └── tests/
│
├── frontend/
├── docs/
├── samples/
├── scripts/
└── README.md
```

---

# Design Principles

The project follows the following architectural principles:

- Clean Architecture
- SOLID Principles
- CQRS
- Repository Pattern
- Ambient Transactions
- Dependency Factories
- Provider-based Integrations
- Async First
- Strong Typing
- Separation of Concerns
- Single Responsibility Principle

---

# Database

Current Database

- PostgreSQL

ORM

- SQLAlchemy Async

Migration

- Alembic

Features

- UUID Primary Keys
- Connection Pooling
- Transaction Management
- Soft Delete Ready

---

# API Response Format

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

# Current APIs

## Health

```
GET /api/v1/health
```

Returns application health information.

---

## Upload Document

```
POST /api/v1/documents/upload
```

Uploads a supported document into the system.

Current supported format:

- PDF

---

# Development Workflow

Current workflow:

```text
Controller
      │
      ▼
Command
      │
      ▼
Service
      │
      ▼
Repository
      │
      ▼
Database
```

Every write operation executes inside a transaction using the `@transactional` decorator.

---

# Documentation

Project documentation is available inside the `docs/` directory.

- Architecture
- RAG Pipeline
- API Reference
- Setup Guide
- Engineering Decisions
- Roadmap

---

# Development Roadmap

## Phase 1

- ✅ Backend Foundation
- ✅ Upload API
- ✅ Repository Layer
- ✅ Transaction Management

---

## Phase 2

- PDF Parser
- Document Metadata
- Chunking

---

## Phase 3

- Embeddings
- ChromaDB
- Semantic Search

---

## Phase 4

- Chat
- Prompt Builder
- Conversation Memory

---

## Phase 5

- Authentication
- Multi-user Support
- Provider Plugins
- Monitoring

---

# License

MIT License

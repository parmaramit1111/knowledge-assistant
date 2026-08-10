````markdown
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
          │                             │
          ▼                             ▼
    Provider Factory               Database
          │
          ▼
        Provider
```
````

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

### Production Database

- AWS RDS PostgreSQL 18

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

The production database is managed outside the application containers.

---

# Document Storage

## Development

Local development supports filesystem-based storage:

```text
backend/storage/
```

This storage is intended for development and testing only.

## Production

Production document storage uses a **private AWS S3 bucket**.

```text
FastAPI
    │
    ▼
Storage Service
    │
    ▼
S3 Storage Provider
    │
    ▼
Private AWS S3 Bucket
```

The application containers should not be used for persistent document storage.

The S3 bucket should use:

- Block Public Access
- Server-side encryption
- IAM-based access
- Restricted bucket permissions

Application access to private documents should be controlled through backend authorization and short-lived access mechanisms where required.

---

# LLM Runtime

The LLM runtime is intentionally separated from the core application deployment.

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

Ollama is an optional external runtime and is not required to run as part of the core application Compose stack.

This allows each deployment to select an appropriate LLM based on:

- Client requirements
- Model quality
- Context requirements
- CPU/GPU resources
- Infrastructure cost

For Ollama deployments, the selected model is provisioned separately from the application.

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

# Deployment Architecture

```text
                    Internet
                       │
                       ▼
              ┌─────────────────┐
              │ React + Nginx   │
              │    Frontend     │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │    FastAPI      │
              │    Backend      │
              └────┬────────────┘
                   │
          ┌────────┼─────────┐
          ▼        ▼         ▼
   ┌────────────┐ ┌────────┐ ┌──────────────┐
   │ AWS RDS    │ │Private │ │ LLM Provider │
   │ PostgreSQL │ │ S3     │ │              │
   │ + pgvector │ │Documents│ │ Ollama /     │
   └────────────┘ └────────┘ │ OpenAI / ... │
                              └──────────────┘
```

The application containers are designed to remain stateless while persistent data is managed by AWS services.

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

### Completed

- Docker Backend Configuration
- Docker Frontend Configuration
- Nginx Configuration
- Docker Compose Configuration
- AWS RDS Architecture
- Private S3 Architecture
- Separate LLM Runtime Architecture
- Database Migration Script
- Health Check Script
- Local Development Setup Scripts

### In Progress

- S3 Storage Provider
- Production Environment Configuration
- Deployment Validation

### Planned

- CI/CD
- Unit Tests
- Integration Tests
- Monitoring
- Metrics
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

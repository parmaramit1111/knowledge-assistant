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
- Provider Independence

---

# Project Structure

```text
backend/
│
├── app/
│
├── api/
├── commands/
├── core/
├── dtos/
├── models/
├── providers/
│   ├── parsers/
│   ├── chunkers/
│   ├── embeddings/
│   ├── prompts/
│   └── llm/
├── queries/
├── repositories/
├── schemas/
├── services/
├── workers/
└── utils/

migrations/
storage/
tests/
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

```
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

#### Prompts

- Default Prompt Provider

#### Large Language Models

- Ollama (`qwen2.5:1.5b`)

### Future Providers

#### Embeddings

- Ollama Embeddings
- OpenAI Embeddings

#### Prompts

- Technical Support Prompt
- FAQ Prompt
- Customer Support Prompt

#### LLMs

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

Business workflow never depends on concrete provider implementations.

---

# Repositories

**Location**

```
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
LLM Provider
    │
    ▼
Grounded AI Response
```

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
- Ollama
- OpenAI

### Prompts

- Default Prompt
- Custom Prompt (Future)

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

Adding a new provider requires no changes to business workflows.

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

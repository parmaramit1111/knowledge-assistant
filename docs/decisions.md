# Engineering Decisions

## Decision 001

### CQRS

**Reason**

Separate read operations from write operations to simplify business logic and improve maintainability.

**Decision**

Use CQRS throughout the application.

---

## Decision 002

### Repository Pattern

**Reason**

Isolate persistence logic from business logic and provide a consistent data access layer.

**Decision**

All database access is performed through repositories derived from the generic `BaseRepository`.

---

## Decision 003

### ExecutionContext

**Reason**

Provide a single execution container responsible for creating and managing the database session, repositories, and services for each request or background task.

**Decision**

Use `ExecutionContext` as the application's dependency and execution scope mechanism.

---

## Decision 004

### Transaction Management

**Reason**

Ensure each command executes within an isolated transaction while keeping transaction handling transparent to business logic.

**Decision**

Commands execute inside transactional boundaries using `ExecutionContext` and the `@transactional` decorator.

---

## Decision 005

### Workflow Services

**Reason**

Separate business workflow orchestration from provider implementations and persistence.

**Decision**

Workflow services coordinate repositories, provider services, and document state transitions.

### Examples

- DocumentWorkflowService
- DocumentProcessingService
- DocumentChunkingService
- DocumentEmbeddingService
- DocumentSearchService
- DocumentChatService

---

## Decision 006

### Provider Services

**Reason**

Separate provider execution and transformation logic from business workflow orchestration.

**Decision**

Provider services are responsible for selecting and executing provider implementations.

### Examples

- DocumentParserService
- DocumentChunkerService
- DocumentEmbedderService
- QueryEmbedderService
- PromptBuilderService
- LLMService

Provider services never perform persistence.

---

## Decision 007

### Factory Pattern

**Reason**

Support multiple interchangeable implementations without changing business workflow.

**Decision**

Use factories to resolve provider implementations.

### Current Factories

- ParserFactory
- ChunkerFactory
- EmbeddingFactory
- PromptFactory
- LLMFactory

Factories isolate provider selection from business workflow.

---

## Decision 008

### Background Workers

**Reason**

Document processing stages are potentially long-running operations and should execute asynchronously.

**Decision**

Each processing stage is implemented as an independent background worker.

### Current Workers

- DocumentWorker
- ChunkWorker
- EmbeddingWorker

Each worker operates within its own `ExecutionContext` and transaction boundary.

---

## Decision 009

### Standard API Response

**Reason**

Provide a consistent API contract across all endpoints.

**Decision**

Every endpoint returns the standard `ApiResponse` model.

Example:

```json
{
  "code": "...",
  "success": true,
  "message": "...",
  "result": {}
}
```

---

## Decision 010

### UUID Primary Keys

**Reason**

Support distributed systems while avoiding sequential identifiers.

**Decision**

Use UUIDs as primary keys for application entities.

---

## Decision 011

### Async SQLAlchemy

**Reason**

Improve scalability and maximize asynchronous request throughput.

**Decision**

Use SQLAlchemy Async with PostgreSQL throughout the application.

---

## Decision 012

### Provider Independence

**Reason**

Allow new parsers, chunkers, embedding providers, prompt providers, vector databases, and LLMs to be added without modifying the core business workflow.

**Decision**

External integrations are implemented behind provider interfaces and factories.

Current provider categories include:

- Document Parsers
- Document Chunkers
- Embeddings
- Prompt Providers
- LLM Providers

---

## Decision 013

### Single Responsibility Services

**Reason**

Keep services small, focused, and easy to maintain and test.

**Decision**

Every processing stage is divided into two service types:

- Workflow Service
- Provider Service

Workflow services orchestrate the process.

Provider services handle provider-specific execution and transformations.

Repositories handle persistence.

---

## Decision 014

### Processing Pipeline

**Reason**

Create a predictable and extensible document ingestion pipeline.

**Decision**

Every document processing stage follows the same architectural pattern.

```text
Worker
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
Factory
   │
   ▼
Provider
   │
   ▼
Repository
```

This pattern is used for:

- Parsing
- Chunking
- Embeddings

---

## Decision 015

### PostgreSQL + pgvector

**Reason**

Provide a relational database with native vector similarity search capabilities for the RAG pipeline.

**Decision**

Use PostgreSQL with the `pgvector` extension for document metadata, chunks, embeddings, and semantic search.

The same architecture can support other vector databases through provider abstractions in the future.

---

## Decision 016

### Sentence Transformer Embeddings

**Reason**

Provide a local, cost-effective embedding model for the reference RAG implementation.

**Decision**

Use Sentence Transformers with:

```text
Model: all-MiniLM-L6-v2
Dimensions: 384
```

The embedding architecture remains provider-independent.

---

## Decision 017

### Ollama as Initial LLM Provider

**Reason**

Provide a local LLM runtime without requiring a paid external AI API for the reference implementation.

**Decision**

Use Ollama as the initial LLM provider.

Current model:

```text
qwen2.5:1.5b
```

LLM integration is isolated behind `LLMService`, `LLMFactory`, and the LLM provider abstraction.

---

## Decision 018

### Prompt Provider Architecture

**Reason**

Separate prompt construction from the LLM implementation and allow prompts to evolve independently.

**Decision**

Use a dedicated Prompt Builder Service and Prompt Provider architecture.

Current implementation:

- PromptBuilderService
- PromptFactory
- Default Prompt Provider

---

## Decision 019

### Local Document Storage for Reference Implementation

**Reason**

Keep the showcase project simple and runnable locally without requiring cloud infrastructure.

**Decision**

Use local filesystem storage for the reference implementation.

```text
backend/storage/
```

Production cloud storage such as AWS S3 is intentionally outside the scope of this showcase project.

---

## Decision 020

### React + TypeScript Frontend

**Reason**

Provide a modern, strongly typed frontend demonstrating full-stack integration with the RAG backend.

**Decision**

Use:

- React
- TypeScript
- Vite
- Material UI

The frontend communicates with the FastAPI backend through dedicated API services and custom hooks.

---

## Decision 021

### Frontend API Separation

**Reason**

Keep API communication separate from UI components and make frontend behavior easier to maintain and test.

**Decision**

Use dedicated API services and custom hooks.

Examples:

```text
useChat
    │
    ▼
Chat API Service
    │
    ▼
FastAPI
```

```text
useDocumentUpload
    │
    ▼
Document API Service
    │
    ▼
FastAPI
```

---

## Decision 022

### CORS Configuration

**Reason**

Allow the React development frontend to communicate with the FastAPI backend while maintaining explicit cross-origin configuration.

**Decision**

Configure CORS at the FastAPI application layer using environment-specific allowed origins.

---

## Decision 023

### Clean Architecture Focus

**Reason**

The primary purpose of the project is to demonstrate engineering ability through architecture, coding practices, RAG implementation, provider abstraction, and technical decision-making.

**Decision**

Keep the project focused on the RAG reference implementation rather than expanding it into a complete production SaaS platform.

Production concerns such as:

- Authentication
- Multi-tenancy
- CI/CD
- Monitoring
- Production infrastructure
- Cloud storage
- Advanced security
- Production scaling

are outside the scope of this showcase implementation.

---

## Decision 024

### Provider-Agnostic RAG Architecture

**Reason**

Demonstrate how the core RAG workflow can remain stable while underlying technologies and providers change.

**Decision**

The core workflow is designed around replaceable providers for:

```text
Document Parsing
       │
       ▼
Chunking
       │
       ▼
Embeddings
       │
       ▼
Vector Search
       │
       ▼
Prompt Generation
       │
       ▼
LLM
```

A provider can be replaced without redesigning the complete application workflow.

---

## Decision 025

### Showcase Project Scope

**Reason**

The project is intended to demonstrate practical engineering skills, architectural thinking, coding standards, RAG implementation, and full-stack development rather than serve as a production SaaS platform.

**Decision**

The showcase scope is considered complete when the following are demonstrated:

- Clean backend architecture
- CQRS
- Repository Pattern
- ExecutionContext
- Workflow Services
- Provider Services
- Factory Pattern
- Background Workers
- Document ingestion
- Document parsing
- Document chunking
- Embeddings
- pgvector semantic search
- Prompt construction
- LLM integration
- Grounded RAG responses
- Source references
- React frontend
- Document upload UI
- Chat UI
- API integration
- Clear engineering documentation

The architecture and implementation can later serve as the foundation for a separate private production RAG platform.

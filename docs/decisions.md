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

Provide a single dependency container responsible for creating and managing the database session, repositories, and services for each request or background task.

**Decision**

Use `ExecutionContext` as the application's dependency management mechanism.

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

Examples

- DocumentWorkflowService
- DocumentProcessingService
- DocumentChunkingService

---

## Decision 006

### Provider Services

**Reason**

Separate business transformations from orchestration.

**Decision**

Provider services are responsible only for selecting and executing providers.

Examples

- DocumentParserService
- DocumentChunkerService

Provider services never perform persistence.

---

## Decision 007

### Factory Pattern

**Reason**

Support multiple interchangeable implementations without changing business logic.

**Decision**

Use factories to resolve providers.

Examples

- ParserFactory
- ChunkerFactory
- EmbeddingFactory (Future)

---

## Decision 008

### Background Workers

**Reason**

Document processing stages are long-running operations and should execute asynchronously.

**Decision**

Each processing stage is implemented as an independent background worker.

Current

- DocumentWorker
- ChunkWorker

Future

- EmbeddingWorker

---

## Decision 009

### Response Wrapper

**Reason**

Provide a consistent API contract across all endpoints.

**Decision**

Every endpoint returns the standard `ApiResponse` model.

---

## Decision 010

### UUID Primary Keys

**Reason**

Support distributed systems while avoiding sequential identifiers.

**Decision**

Use UUIDs as primary keys for all entities.

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

Allow new parsers, chunkers, embedding providers, vector databases, and LLMs to be added without modifying business workflow.

**Decision**

All external integrations are implemented behind provider interfaces and factories.

---

## Decision 013

### Single Responsibility Services

**Reason**

Keep services small, focused, and easy to test.

**Decision**

Every processing stage is divided into two service types:

- Workflow Service
- Provider Service

Workflow services orchestrate the process.

Provider services perform the business transformation.

---

## Decision 014

### Processing Pipeline

**Reason**

Create a predictable and extensible document ingestion pipeline.

**Decision**

Every processing stage follows the same architecture.

```text
Worker

↓

Command

↓

Workflow Service

↓

Provider Service

↓

Factory

↓

Provider
```

This pattern is used for:

- Parsing
- Chunking
- Embeddings (Future)

# RAG Pipeline

## Purpose

The Retrieval-Augmented Generation (RAG) pipeline transforms uploaded documents into searchable knowledge that can be retrieved and used to generate accurate, context-aware AI responses.

The pipeline is implemented incrementally, with each stage having a single responsibility and remaining independent from the others. This modular architecture allows new providers and technologies to be introduced without changing the overall workflow.

---

# Pipeline Overview

```text
Upload Document
        │
        ▼
Parse Document
        │
        ▼
Chunk Document
        │
        ▼
Generate Embeddings
        │
        ▼
Store in PostgreSQL (pgvector)
        │
        ▼
Semantic Search
        │
        ▼
Prompt Builder
        │
        ▼
Large Language Model
        │
        ▼
Grounded AI Response
```

---

# Current Project Status

| Stage                     | Status       |
| ------------------------- | ------------ |
| Upload                    | ✅ Completed |
| Parsing                   | ✅ Completed |
| Chunking                  | ✅ Completed |
| Embeddings                | ✅ Completed |
| Vector Storage (pgvector) | ✅ Completed |
| Semantic Search           | ✅ Completed |
| Prompt Builder            | ✅ Completed |
| AI Chat                   | ✅ Completed |
| Frontend Chat UI          | ✅ Completed |
| Document Upload UI        | ✅ Completed |

---

# Processing Pipeline

Every processing stage follows the same architecture.

```text
Scheduler
        │
        ▼
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

This keeps each processing stage modular, testable, and provider-independent.

---

# Pipeline Stages

## Stage 1 — Document Upload ✅

### Responsibilities

- Receive uploaded documents
- Validate supported file types
- Store original documents
- Create document record
- Initialize processing workflow

### Supported Formats

- PDF
- DOCX
- TXT
- HTML
- Markdown

### Output

```text
Document
```

---

## Stage 2 — Document Parsing ✅

### Responsibilities

- Select the appropriate parser
- Extract document content
- Persist ParsedDocument
- Update document workflow

### Current Parsers

- PDF Parser
- Word Parser
- Text Parser
- HTML Parser
- Markdown Parser

### Future Enhancements

- Metadata Extraction
- OCR Support

### Output

```text
ParsedDocument
```

---

## Stage 3 — Document Chunking ✅

### Responsibilities

- Split parsed documents into semantic chunks
- Persist document chunks
- Update chunk workflow

### Current Strategy

- Recursive Character Splitter
- Chunk Size: **800**
- Chunk Overlap: **200**
- Custom Separators

### Future Strategies

- Semantic Splitter
- Markdown Splitter
- Token Splitter

### Output

```text
DocumentChunk[]
```

---

## Stage 4 — Embeddings ✅

### Responsibilities

- Generate vector embeddings for every document chunk
- Generate embeddings for user queries
- Persist embeddings using pgvector
- Track embedding workflow
- Store embedding metadata

### Current Provider

- Sentence Transformers
  - Model: `all-MiniLM-L6-v2`
  - Dimensions: **384**

### Future Providers

- Ollama Embeddings
- OpenAI Embeddings
- Additional Embedding Providers

### Output

```text
DocumentChunkEmbedding[]
```

---

## Stage 5 — Semantic Search ✅

### Responsibilities

- Convert user queries into embeddings
- Perform cosine similarity search
- Retrieve Top-K relevant document chunks
- Rank results by similarity score
- Return document metadata with search results

### Current Implementation

- PostgreSQL + pgvector
- Cosine Similarity Search
- Sentence Transformer Query Embeddings
- Search API
- Ranked Search Results

### Future Enhancements

- Metadata Filtering
- Hybrid Search
- Re-ranking

### Output

```text
Relevant Document Chunks
```

---

## Stage 6 — Prompt Builder ✅

### Responsibilities

- Build prompts using retrieved context
- Inject document chunks into the prompt
- Apply prompt templates
- Add user question
- Prepare prompts for LLM providers

### Current Implementation

- Prompt Builder Service
- Prompt Provider Architecture
- Prompt Factory
- Default Prompt Provider
- Context Assembly
- Context Injection
- Source Attribution
- Source-aware Prompt Generation

### Future Enhancements

- Conversation History
- Token Budget Management
- Multiple Prompt Templates
- Domain-specific Prompt Providers

### Output

```text
LLM Prompt
```

---

## Stage 7 — AI Chat ✅

### Responsibilities

- Receive user questions
- Retrieve relevant document context
- Generate grounded AI responses
- Return source document references

### Current Implementation

- Chat API
- AskQuestion Command
- DocumentChatService
- LLMService
- LLM Provider Architecture
- LLM Factory
- Ollama Provider
- Local LLM Integration
- Grounded AI Responses
- Source References
- End-to-End RAG Chat Pipeline

### Current LLM Provider

- Ollama
  - Model: `qwen2.5:1.5b`

### Future Providers

- OpenAI
- Anthropic
- Gemini
- Azure OpenAI

### Output

```text
Grounded AI Response
```

---

# Stage 8 — Frontend Experience ✅

The frontend provides the user-facing interface for interacting with the RAG platform.

### Current Implementation

- React
- TypeScript
- Vite
- Material UI
- Chat Interface
- Chat API Integration
- Conversation State Management
- Source References
- New Chat
- Sidebar Navigation
- Collapsible Sidebar
- PDF Document Upload
- Drag & Drop Upload
- Upload Success/Error Handling
- Application Theme
- Knowledge Assistant Branding
- Backend CORS Integration

### Frontend Architecture

```text
User
 │
 ▼
React Page
 │
 ▼
UI Components
 │
 ▼
Custom Hooks
 │
 ▼
API Services
 │
 ▼
FastAPI
```

### Current Frontend API Integration

```text
Chat UI
   │
   ▼
useChat
   │
   ▼
chat.ts
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
document.ts
   │
   ▼
POST /api/v1/documents/upload
```

---

# Background Processing

Long-running stages execute asynchronously.

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

Future processing stages will follow the same background execution model.

---

# Architecture Principles

The RAG pipeline follows these principles.

- Single Responsibility Principle
- Provider Independence
- Workflow Separation
- Background Processing
- Factory Pattern
- CQRS
- ExecutionContext
- Workflow Services
- Provider Services
- Async First Design
- Strong Typing

Each stage consumes the output produced by the previous stage and remains independent of the underlying provider implementation.

---

# Current End-to-End Pipeline

```text
                    DOCUMENT INGESTION
                           │
                           ▼
                      Upload API
                           │
                           ▼
                       Document
                           │
                           ▼
                    DocumentWorker
                           │
                           ▼
                    Document Parser
                           │
                           ▼
                    ParsedDocument
                           │
                           ▼
                      ChunkWorker
                           │
                           ▼
                     DocumentChunk
                           │
                           ▼
                   EmbeddingWorker
                           │
                           ▼
                 Sentence Transformer
                           │
                           ▼
             DocumentChunkEmbedding
                           │
                           ▼
                 PostgreSQL (pgvector)
                           │
                           │
                           │
                    USER QUESTION
                           │
                           ▼
                       Chat API
                           │
                           ▼
                   Query Embedding
                           │
                           ▼
                   Semantic Search
                           │
                           ▼
                  Relevant Chunks
                           │
                           ▼
                    Prompt Builder
                           │
                           ▼
                    LLM Provider
                           │
                           ▼
                 Grounded AI Response
                           │
                           ▼
                  Source References
                           │
                           ▼
                     React Chat UI
```

---

# Current Query Architecture

```text
User Question
      │
      ▼
Chat API
      │
      ▼
DocumentChatService
      │
      ├──────────────► DocumentSearchService
      │                       │
      │                       ▼
      │                 Query Embedding
      │                       │
      │                       ▼
      │                 Semantic Search
      │
      ├──────────────► PromptBuilderService
      │                       │
      │                       ▼
      │                 Prompt Provider
      │
      └──────────────► LLMService
                              │
                              ▼
                         LLM Provider
                              │
                              ▼
                     Grounded Response
                              │
                              ▼
                       Source References
```

---

# Provider Architecture

The RAG pipeline is designed around provider abstractions.

```text
                    Provider Interface
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
       Provider A       Provider B       Provider C
```

### Parser Providers

- PDF
- DOCX
- TXT
- HTML
- Markdown

### Chunking Providers

- Recursive Character Splitter
- Semantic Splitter
- Markdown Splitter
- Token Splitter

### Embedding Providers

- Sentence Transformers
- Ollama
- OpenAI

### Prompt Providers

- Default Prompt
- Custom Prompt

### LLM Providers

- Ollama
- OpenAI
- Anthropic
- Gemini
- Azure OpenAI

New providers can be introduced behind the existing provider architecture without changing the core workflow.

---

# Production Readiness

The core RAG pipeline and frontend experience are complete.

The production-readiness phase is now focused on deployment infrastructure, cloud storage, configuration, and operational readiness.

### Completed

- Backend Docker Configuration
- Frontend Docker Configuration
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

# Long-Term Vision

The Knowledge Assistant is designed as a provider-agnostic RAG platform capable of supporting:

- Multiple document formats
- Multiple parsing providers
- Multiple chunking strategies
- Multiple embedding providers
- Multiple prompt providers
- Multiple vector databases
- Multiple Large Language Models
- Multiple frontend deployment environments

The architecture allows new providers and technologies to be introduced with minimal changes to the business workflow while maintaining a clean, modular, testable, and extensible design.

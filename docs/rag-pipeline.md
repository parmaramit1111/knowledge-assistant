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
Store in Vector Database
        │
        ▼
Semantic Retrieval
        │
        ▼
Prompt Builder
        │
        ▼
Large Language Model
        │
        ▼
AI Response
```

---

# Current Project Status

| Stage           | Status            |
| --------------- | ----------------- |
| Upload          | ✅ Completed      |
| Parsing         | ✅ Completed      |
| Chunking        | ✅ Completed      |
| Embeddings      | 🚧 Next Milestone |
| Vector Database | Planned           |
| Retrieval       | Planned           |
| Prompt Builder  | Planned           |
| AI Chat         | Planned           |

---

# Processing Pipeline

Every stage follows the same architecture.

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

This keeps each processing stage modular, testable, and provider-independent.

---

# Pipeline Stages

## Stage 1 — Document Upload ✅

Responsibilities

- Receive uploaded documents
- Validate file type
- Store documents
- Create document record

Supported Formats

- PDF
- DOCX
- TXT
- HTML
- Markdown

Output

```text
Document
```

---

## Stage 2 — Document Parsing ✅

Responsibilities

- Select appropriate parser
- Extract document content
- Store ParsedDocument
- Update workflow status

Current Parsers

- PDF Parser
- Word Parser
- Text Parser
- HTML Parser
- Markdown Parser

Future Enhancements

- Metadata Extraction
- OCR Support

Output

```text
ParsedDocument
```

---

## Stage 3 — Document Chunking ✅

Responsibilities

- Split parsed documents into semantic chunks
- Persist document chunks
- Update workflow status

Current Strategy

- Recursive Character Splitter

Future Strategies

- Semantic Splitter
- Markdown Splitter
- Token Splitter

Output

```text
DocumentChunk[]
```

---

## Stage 4 — Embeddings 🚧

Responsibilities

- Generate embeddings for every document chunk
- Persist vector representations
- Update embedding workflow

Planned Providers

- Sentence Transformers
- Ollama Embeddings
- OpenAI Embeddings

Output

```text
Embedded Document Chunks
```

---

## Stage 5 — Vector Storage

Responsibilities

- Store embeddings
- Store searchable metadata
- Enable semantic similarity search

Planned Vector Databases

- ChromaDB
- PGVector
- Milvus
- Qdrant

Output

```text
Vector Index
```

---

## Stage 6 — Semantic Retrieval

Responsibilities

- Convert user query into embedding
- Search similar document chunks
- Apply metadata filtering
- Rank search results

Future Features

- Hybrid Search
- Metadata Filtering
- Re-ranking

Output

```text
Relevant Document Chunks
```

---

## Stage 7 — Prompt Builder

Responsibilities

- Assemble retrieved context
- Apply prompt templates
- Respect token limits
- Build final LLM prompt

Output

```text
Prompt
```

---

## Stage 8 — AI Response

Responsibilities

- Send prompt to configured LLM
- Generate grounded response
- Return references and citations

Planned Providers

- Ollama
- OpenAI
- Anthropic
- Gemini

Output

```text
AI Response
```

---

# Background Processing

Long-running stages execute asynchronously.

```text
Scheduler

↓

Worker

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

---

# Architecture Principles

The RAG pipeline follows these principles.

- Single Responsibility
- Provider Independence
- Workflow Separation
- Background Processing
- Factory Pattern
- ExecutionContext
- Workflow Services
- Provider Services

Each stage consumes only the output of the previous stage and remains independent of the underlying provider implementation.

---

# Long-Term Vision

The Knowledge Assistant is designed to become a provider-agnostic enterprise RAG platform capable of supporting:

- Multiple document formats
- Multiple chunking strategies
- Multiple embedding providers
- Multiple vector databases
- Multiple Large Language Models

The architecture allows new providers to be introduced with minimal changes to business workflow.

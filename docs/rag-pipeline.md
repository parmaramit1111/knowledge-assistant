# RAG Pipeline

## Purpose

The RAG pipeline transforms uploaded documents into searchable knowledge that can be used to answer user questions.

The pipeline is implemented incrementally following the project roadmap. Each stage has a single responsibility and can evolve independently.

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
Retrieve Relevant Chunks
        │
        ▼
Build Prompt
        │
        ▼
Generate AI Response
```

---

# Development Roadmap Alignment

| Milestone   | Pipeline Stage               |
| ----------- | ---------------------------- |
| Milestone 2 | Upload Document              |
| Milestone 3 | Parse Document               |
| Milestone 4 | Chunk Document               |
| Milestone 5 | Embeddings + Vector Database |
| Milestone 6 | Retrieval + Prompt + LLM     |
| Milestone 7 | Chat Experience              |

---

# Pipeline Stages

## Stage 1 — Upload

Responsibilities

- Receive uploaded document
- Validate uploaded file
- Manage file storage
- Return upload result

Supported format (MVP)

- PDF

---

## Stage 2 — Document Parsing

Responsibilities

- Parse uploaded PDF
- Extract document content
- Return a ParsedDocument

The parser is responsible only for document parsing.

It is not responsible for:

- Chunking
- Embeddings
- Storage
- AI processing

---

## Stage 3 — Chunking

Responsibilities

- Split parsed document into chunks
- Support configurable chunking strategies

---

## Stage 4 — Embeddings

Responsibilities

- Generate vector embeddings for document chunks

Initial provider

- Sentence Transformers

---

## Stage 5 — Vector Storage

Responsibilities

- Store document chunks and embeddings

Initial database

- ChromaDB

---

## Stage 6 — Retrieval & Generation

Responsibilities

- Retrieve relevant chunks
- Build prompt
- Generate grounded response using the configured LLM

Initial LLM

- Ollama

---

# Architecture Principles

- Every pipeline stage has a single responsibility.
- Each stage consumes the output of the previous stage.
- Pipeline stages remain loosely coupled.
- Providers contain integration logic only.
- Business orchestration belongs in the service layer.

---

# Current Milestone

We are currently implementing:

**Milestone 2 — Document Upload**

Current scope:

- PDF upload endpoint
- File validation
- Upload management
- Local storage

Document parsing begins in the next milestone.

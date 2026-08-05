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
AI Response
```

---

# Current Project Status

| Stage                     | Status         |
| ------------------------- | -------------- |
| Upload                    | ✅ Completed   |
| Parsing                   | ✅ Completed   |
| Chunking                  | ✅ Completed   |
| Embeddings                | ✅ Completed   |
| Vector Storage (pgvector) | ✅ Completed   |
| Semantic Search           | ✅ Completed   |
| Prompt Builder            | 🚧 In Progress |
| AI Chat                   | Planned        |

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
- Persist embeddings using pgvector
- Track embedding workflow
- Store embedding metadata

### Current Provider

- Sentence Transformers
  - Model: `all-MiniLM-L6-v2`
  - Dimensions: 384

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

## Stage 6 — Prompt Builder 🚧

### Responsibilities

- Assemble retrieved context
- Apply prompt templates
- Respect token limits
- Build the final LLM prompt
- Attach source references

### Output

```text
Prompt
```

---

## Stage 7 — AI Response

### Responsibilities

- Send prompt to the configured LLM
- Generate grounded responses
- Return references and citations

### Planned Providers

- Ollama
- OpenAI
- Anthropic
- Gemini

### Output

```text
AI Response
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

Each stage consumes only the output produced by the previous stage and remains independent of the underlying provider implementation.

---

# Current Pipeline

```text
Upload
   │
   ▼
Document
   │
   ▼
DocumentWorker
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
SentenceTransformer
   │
   ▼
DocumentChunkEmbedding (pgvector)
   │
   ▼
Semantic Search
   │
   ▼
READY FOR PROMPT BUILDER
```

---

# Long-Term Vision

The Knowledge Assistant is designed to become a provider-agnostic enterprise RAG platform capable of supporting:

- Multiple document formats
- Multiple parsing providers
- Multiple chunking strategies
- Multiple embedding providers
- Multiple vector databases
- Multiple Large Language Models

The architecture allows new providers and technologies to be introduced with minimal changes to the business workflow while maintaining a clean, modular, and extensible design.

# API Guidelines

## Base URL

```text
/api/v1
```

---

# Authentication

Authentication is currently **not implemented**.

---

# Standard Response

Successful API responses follow the standard response structure:

```json
{
  "code": "...",
  "success": true,
  "message": "...",
  "result": {}
}
```

---

# Error Response

API errors use the standard response structure with `success` set to `false`.

```json
{
  "code": "...",
  "success": false,
  "message": "...",
  "result": null
}
```

---

# Health API

## Check Application Health

```http
GET /api/v1/health
```

### Purpose

Returns the current health status of the Knowledge Assistant backend.

---

# Document APIs

## Upload Document

```http
POST /api/v1/documents/upload
```

### Purpose

Uploads a document and initializes the document processing workflow.

### Supported Types

- PDF
- DOCX
- TXT
- HTML
- Markdown

### Processing Flow

```text
Upload
   │
   ▼
Document
   │
   ▼
Parse
   │
   ▼
Chunk
   │
   ▼
Generate Embeddings
   │
   ▼
Store in PostgreSQL (pgvector)
```

---

# Search API

## Semantic Search

```http
POST /api/v1/search
```

### Purpose

Performs semantic similarity search against the document embeddings stored in PostgreSQL with pgvector.

### Processing Flow

```text
Search Query
     │
     ▼
Query Embedding
     │
     ▼
PGVector Similarity Search
     │
     ▼
Ranked Results
     │
     ▼
Document Metadata
```

---

# Chat API

## Ask Question

```http
POST /api/v1/chat
```

### Purpose

Generates a grounded AI response using relevant document context retrieved through the RAG pipeline.

### Processing Flow

```text
User Question
      │
      ▼
Query Embedding
      │
      ▼
Semantic Search
      │
      ▼
Relevant Document Chunks
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
```

---

# API Architecture

```text
Client
   │
   ▼
FastAPI
   │
   ▼
API Controller
   │
   ▼
Command / Query
   │
   ▼
Workflow Service
   │
   ├──────────────► Provider Service
   │
   └──────────────► Repository
                         │
                         ▼
                    PostgreSQL
```

---

# Frontend Integration

The React frontend communicates with the backend through dedicated API services.

### Chat

```text
Chat UI
   │
   ▼
useChat
   │
   ▼
Chat API Service
   │
   ▼
POST /api/v1/chat
```

### Document Upload

```text
Document Upload UI
   │
   ▼
useDocumentUpload
   │
   ▼
Document API Service
   │
   ▼
POST /api/v1/documents/upload
```

---

# Current API Summary

| API                        | Method | Purpose                  |
| -------------------------- | ------ | ------------------------ |
| `/api/v1/health`           | GET    | Application health       |
| `/api/v1/documents/upload` | POST   | Upload documents         |
| `/api/v1/search`           | POST   | Semantic document search |
| `/api/v1/chat`             | POST   | Grounded RAG chat        |

---

# API Documentation

FastAPI provides interactive API documentation through:

```text
http://localhost:8000/docs
```

Alternative OpenAPI documentation:

```text
http://localhost:8000/redoc
```

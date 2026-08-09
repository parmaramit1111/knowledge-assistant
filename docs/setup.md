# Development Setup

## Requirements

- Python 3.12+
- PostgreSQL
- Git

## Clone

git clone ...

## Create Virtual Environment

python -m venv .venv

source .venv/bin/activate

## Install Dependencies

pip install -r requirements.txt

## Environment Variables

cp .env.example .env

Update:

DATABASE_URL
OPENAI_API_KEY
...

## Database

alembic upgrade head

## Run

uvicorn app.main:app --reload

## Background Worker

python -m app.workers.scheduler

## API Documentation

http://localhost:8000/docs

# Frontend Development Setup

## Requirements

- Node.js 20+
- npm 10+
- Git
- Backend API running locally

## Frontend Structure

```text
frontend/
├── public/
│   └── assets/
│       └── logo/
├── src/
│   ├── api/
│   │   ├── models/
│   │   ├── chat.ts
│   │   └── document.ts
│   ├── components/
│   │   ├── chat/
│   │   ├── common/
│   │   └── documents/
│   ├── hooks/
│   │   ├── useChat.ts
│   │   └── useDocumentUpload.ts
│   ├── pages/
│   │   └── ChatPage.tsx
│   ├── App.tsx
│   ├── main.tsx
│   └── theme.ts
├── index.html
├── package.json
├── tsconfig.json
└── vite.config.ts
```

## Install Dependencies

From the repository root:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

## Environment Variables

Create a local environment file:

```bash
touch .env
```

Add:

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

The frontend reads the API base URL using Vite's environment variable system:

```typescript
import.meta.env.VITE_API_BASE_URL;
```

If `VITE_API_BASE_URL` is not configured, the application falls back to:

```text
/api/v1
```

## Start Development Server

```bash
npm run dev
```

The Vite development server will normally be available at:

```text
http://localhost:5173
```

## Backend

Start the FastAPI backend separately:

```bash
cd backend

source .venv/bin/activate

uvicorn app.main:app --reload
```

Backend API:

```text
http://localhost:8000
```

API documentation:

```text
http://localhost:8000/docs
```

## CORS

The backend must allow the frontend development origin.

For local development, the backend should allow:

```text
http://localhost:5173
```

CORS configuration belongs to the backend and is required for browser-based communication between the React frontend and FastAPI API.

## Build

Create a production build:

```bash
npm run build
```

The build performs TypeScript compilation and Vite production bundling.

## TypeScript Validation

Run TypeScript validation independently:

```bash
npx tsc -b
```

## Preview Production Build

After building:

```bash
npm run preview
```

The production build can then be previewed locally using the Vite preview server.

## API Integration

The frontend communicates with the backend through the API layer:

```text
React Component
       │
       ▼
Hook
       │
       ▼
API Service
       │
       ▼
FastAPI
       │
       ▼
PostgreSQL / RAG Pipeline
```

### Current API Services

```text
src/api/
├── chat.ts
└── document.ts
```

### Current APIs

```http
POST /api/v1/chat
```

```http
POST /api/v1/documents/upload
```

## Current Frontend Features

- Chat interface
- Conversation state
- New Chat
- Source references
- PDF upload
- Drag-and-drop PDF upload
- Upload success/error handling
- Sidebar navigation
- Collapsible sidebar
- Material UI theme
- Knowledge Assistant branding

## Development Workflow

Before committing frontend changes:

```bash
npm run build
```

Then verify the working tree:

```bash
git status
```

Review changes:

```bash
git diff
```

Commit changes:

```bash
git add frontend/
git commit -m "feat(frontend): ..."
```

Push the current feature branch:

```bash
git push
```

## Production

Production deployment configuration is intentionally not covered yet.

The next development phase will cover:

- Docker
- Frontend containerization
- Backend containerization
- PostgreSQL configuration
- Environment management
- Production API configuration
- Reverse proxy
- Deployment
- CI/CD
- Monitoring

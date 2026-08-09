Yes, I checked the structure.

### 1. Are we using Next.js?

**No.**

This is a **React + TypeScript + Vite** application:

```text
Vite
  ↓
React
  ↓
TypeScript
```

The presence of `vite.config.ts`, `main.tsx`, and `App.tsx` confirms that.

We should **stay with Vite** for this milestone. No need to convert to Next.js.

---

### 2. Are we using a UI framework?

Yes, I recommend we use **Material UI (MUI)** for the Chat UI.

That gives us:

```text
React
  +
TypeScript
  +
Vite
  +
Material UI
```

We don't need Tailwind or another UI framework.

For this project, MUI is enough for:

- Chat layout
- Message bubbles
- Text field
- Buttons
- Loading indicators
- Cards
- Source references
- Responsive layout

---

# What we do next

The scaffold is good. **Do not create any more files.**

We already have exactly what we need:

```text
src/
├── api/
│   └── chat.ts
├── components/
│   └── chat/
│       ├── ChatContainer.tsx
│       ├── ChatHeader.tsx
│       ├── ChatInput.tsx
│       ├── ChatMessage.tsx
│       └── ChatSources.tsx
├── hooks/
│   └── useChat.ts
├── pages/
│   └── ChatPage.tsx
├── App.tsx
└── main.tsx
```

### Build order

**Step 1 — `package.json`**

Verify/install:

```text
@mui/material
@emotion/react
@emotion/styled
```

**Step 2 — `src/api/chat.ts`**

Create the API call to:

```http
POST /api/v1/chat
```

**Step 3 — Chat types**

We currently don't have a `types/` folder, and I don't think we need to add one yet. Keep the types close to the API/hook until the UI grows.

**Step 4 — `useChat.ts`**

Manage:

```text
conversationId
messages
loading
error
sendMessage()
newConversation()
```

**Step 5 — Components**

Build in this order:

```text
ChatHeader
    ↓
ChatMessage
    ↓
ChatSources
    ↓
ChatInput
    ↓
ChatContainer
```

**Step 6 — `ChatPage.tsx`**

Compose everything.

**Step 7 — `App.tsx`**

Make `ChatPage` the application entry page.

**Step 8 — Run against the real FastAPI backend**

Then validate:

```text
New Chat
   ↓
Question
   ↓
Backend
   ↓
RAG
   ↓
Ollama
   ↓
Answer + Sources
   ↓
Follow-up Question
   ↓
Same conversation_id
   ↓
Chat History
```

### So our immediate next action

**Open `package.json` and share it with me.**

I'll verify the existing dependencies first. Then we'll build **`src/api/chat.ts`**.

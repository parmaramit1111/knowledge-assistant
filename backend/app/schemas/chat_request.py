from uuid import UUID

from pydantic import BaseModel

class ChatRequest(BaseModel):
    question: str
    conversation_id: UUID | None = None
from uuid import UUID

from pydantic import BaseModel

class SourceItem(BaseModel):
    document_name: str

    chunk_index: int

class ChatResponse(BaseModel):
    conversation_id: UUID

    answer: str

    sources: list[SourceItem]

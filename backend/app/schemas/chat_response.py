from pydantic import BaseModel

class SourceItem(BaseModel):
    document_name: str

    chunk_index: int

class ChatResponse(BaseModel):
    answer: str

    sources: list[SourceItem]

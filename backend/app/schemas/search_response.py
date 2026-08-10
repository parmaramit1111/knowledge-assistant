from uuid import UUID

from pydantic import BaseModel

class SearchResultItem(BaseModel):
    document_id: UUID
    chunk_id: UUID
    document_name: str
    content: str
    similarity_score: float
    chunk_index: int

class SearchResponse(BaseModel):
    results: list[SearchResultItem]
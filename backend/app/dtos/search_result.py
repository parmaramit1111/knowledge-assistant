from dataclasses import dataclass
from uuid import UUID

@dataclass(slots=True)
class SearchResult():
    chunk_id: UUID
    document_id: UUID
    document_name: str
    content: str
    chunk_index: int
    similarity_score: float

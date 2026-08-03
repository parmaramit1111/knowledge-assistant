from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseRepository
from app.models.document_chunk_embedding import DocumentChunkEmbedding

class DocumentChunkEmbeddingRepository(BaseRepository[DocumentChunkEmbedding]):

    def __init__(
        self,
        session: AsyncSession,
    ):
        super().__init__(
            session,
            DocumentChunkEmbedding,
        )

    async def get(self, id: UUID,) -> DocumentChunkEmbedding | None:
        return await self.get_by_id(id)

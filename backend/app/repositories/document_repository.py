from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseRepository
from app.models.document import Document, ParseStatus, ChunkStatus, EmbeddingStatus

class DocumentRepository(BaseRepository[Document]):

    def __init__(
        self,
        session: AsyncSession,
    ):
        super().__init__(
            session,
            Document,
        )

    async def get_pending_for_processing(self, limit: int,):
        return await self.find(
            Document.is_deleted.is_(False),
            Document.parse_status == ParseStatus.PENDING,
            limit=limit,
        )

    async def get_pending_for_chunking(self, limit: int,):
        return await self.find(
            Document.is_deleted.is_(False),
            Document.parse_status == ParseStatus.COMPLETED,
            Document.chunk_status == ChunkStatus.PENDING,
            limit=limit,
        )

    async def get_pending_for_embedding(self, limit: int,):
        return await self.find(
            Document.is_deleted.is_(False),
            Document.parse_status == ParseStatus.COMPLETED,
            Document.chunk_status == ChunkStatus.COMPLETED,
            Document.embedding_status == EmbeddingStatus.PENDING,
            limit=limit,
        )


    async def get_document(self, id: UUID,) -> Document | None:
        return await self.get_by_id(id)

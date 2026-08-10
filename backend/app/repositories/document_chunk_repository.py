from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document import EmbeddingStatus

from .base import BaseRepository
from app.models.document_chunk import DocumentChunk

class DocumentChunkRepository(BaseRepository[DocumentChunk]):

    def __init__(
        self,
        session: AsyncSession,
    ):
        super().__init__(
            session,
            DocumentChunk,
        )

    async def get(self, id: UUID,) -> DocumentChunk | None:
        return await self.get_by_id(id)

    async def get_pending_embeddings(self, document_id: UUID, parsed_document_id: UUID, ) -> list[DocumentChunk]:
        return await self.find(
            DocumentChunk.is_deleted.is_(False),
            DocumentChunk.document_id == document_id,
            DocumentChunk.parsed_document_id == parsed_document_id,
            DocumentChunk.embedding_status == EmbeddingStatus.PENDING,
            limit=1000,
        )

    async def mark_embedding_running(
        self,
        document_chunk: DocumentChunk,
    ) -> DocumentChunk:
        document_chunk.embedding_status = EmbeddingStatus.RUNNING
        return await self.update(document_chunk)

    async def mark_embedding_completed(
        self,
        document_chunk: DocumentChunk,
    ) -> DocumentChunk:
        document_chunk.embedding_status = EmbeddingStatus.COMPLETED
        return await self.update(document_chunk)

    async def mark_embedding_failed(
        self,
        document_chunk: DocumentChunk,
    ) -> DocumentChunk:
        document_chunk.embedding_status = EmbeddingStatus.FAILED
        return await self.update(document_chunk)

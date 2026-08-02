from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

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

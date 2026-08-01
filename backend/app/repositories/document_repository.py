from uuid import UUID

from .base import BaseRepository
from app.models.document import Document, ParseStatus

class DocumentRepository(BaseRepository[Document]):

    def __init__(self):
        super().__init__(Document)

    async def get_pending_for_processing(self, limit: int,):
        return await self.find(
            Document.is_deleted.is_(False),
            Document.parse_status == ParseStatus.PENDING,
            limit=limit,
        )

    async def get_document(self, id: UUID,) -> Document | None:
        return await self.get_by_id(id)

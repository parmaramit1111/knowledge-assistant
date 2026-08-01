from uuid import UUID

from .base import BaseRepository
from app.models.parsed_document import ParsedDocument

class ParsedDocumentRepository(BaseRepository[ParsedDocument]):

    def __init__(self):
        super().__init__(ParsedDocument)

    async def get(self, id: UUID,) -> ParsedDocument | None:
        return await self.get_by_id(id)

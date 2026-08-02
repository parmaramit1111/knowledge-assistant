from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseRepository
from app.models.parsed_document import ParsedDocument

class ParsedDocumentRepository(BaseRepository[ParsedDocument]):

    def __init__(
        self,
        session: AsyncSession,
    ):
        super().__init__(
            session,
            ParsedDocument,
        )

    async def get(self, id: UUID,) -> ParsedDocument | None:
        return await self.get_by_id(id)

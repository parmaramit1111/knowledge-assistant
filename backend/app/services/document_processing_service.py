from uuid import UUID

from app.models.document import Document, DocumentStatus, ParseStatus
from app.services.document_parser_service import DocumentParserService
from app.repositories.document_repository import DocumentRepository

class DocumentProcessingService:

    def __init__(
        self,
        document_repository: DocumentRepository,
        parser_service: DocumentParserService,
    ) -> None:
        self.document_repository =  document_repository
        self.parser_service =  parser_service

    async def get_pending(self,limit:int) -> list[Document]:
        return await self.document_repository.get_pending_for_processing(limit=limit)

    async def get_document(self, id: UUID,) -> Document | None:
        return await self.document_repository.get_document(id)

    async def begin_processing(
        self,
        document_id: UUID,
    ) -> Document | None:

        document = await self.document_repository.get_document(document_id)

        if document is None:
            return None

        document.document_status = DocumentStatus.PROCESSING
        document.parse_status = ParseStatus.RUNNING

        await self.document_repository.update(document)

        return document

    async def mark_parsing_completed(
        self,
        document: Document,
    ) -> Document | None:
        document.document_status = DocumentStatus.READY
        document.parse_status = ParseStatus.COMPLETED

        return await self.document_repository.update(document)

    async def mark_parsing_failed(
        self,
        document: Document,
    ) -> Document | None:
        document.document_status = DocumentStatus.FAILED
        document.parse_status = ParseStatus.FAILED

        return await self.document_repository.update(document)

    async def process_document(
        self,
        document_id: UUID,
    ) -> None:
        document = await self.begin_processing(document_id)

        if document is None:
            return

        try:
            await self.parser_service.parse(document)

            await self.mark_parsing_completed(
                document,
            )
        except Exception:
            await self.mark_parsing_failed(
                document,
            )
            raise
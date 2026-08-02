from functools import cached_property

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal

from app.repositories.document_repository import DocumentRepository
from app.repositories.parsed_document_repository import ParsedDocumentRepository

from app.services.document_upload_service import DocumentUploadService
from app.services.document_parser_service import DocumentParserService
from app.services.document_processing_service import DocumentProcessingService


class ExecutionContext:

    def __init__(self) -> None:
        self._session: AsyncSession | None = None

    async def __aenter__(self):
        self._session = AsyncSessionLocal()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self._session:
            await self._session.close()

    @property
    def session(self) -> AsyncSession:
        if self._session is None:
            raise RuntimeError(
                "ExecutionContext has not been initialized."
            )
        return self._session

    #
    # Repositories
    #

    @cached_property
    def document_repository(self):
        return DocumentRepository(self.session)

    @cached_property
    def parsed_document_repository(self):
        return ParsedDocumentRepository(self.session)

    #
    # Services
    #
    @cached_property
    def document_upload_service(self):
        return DocumentUploadService(
            document_repository=self.document_repository,
        )

    @cached_property
    def document_parser_service(self):
        return DocumentParserService(
            parsed_document_repository=self.parsed_document_repository,
        )

    @cached_property
    def document_processing_service(self):
        return DocumentProcessingService(
            document_repository=self.document_repository,
            parser_service=self.document_parser_service,
        )
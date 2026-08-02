from functools import cached_property

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal

from app.repositories.document_repository import DocumentRepository
from app.repositories.parsed_document_repository import ParsedDocumentRepository
from app.repositories.document_chunk_repository import DocumentChunkRepository

from app.services.document_workflow_service import DocumentWorkflowService
from app.services.document_upload_service import DocumentUploadService
from app.services.document_parser_service import DocumentParserService
from app.services.document_processing_service import DocumentProcessingService
from app.services.document_chunking_service import DocumentChunkingService
from app.services.document_chunker_service import DocumentChunkerService


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

    @cached_property
    def document_chunk_repository(self):
        return DocumentChunkRepository(self.session)

    #
    # Services
    #

    @cached_property
    def document_workflow_service(self):
        return DocumentWorkflowService(
            document_repository=self.document_repository,
        )

    @cached_property
    def document_upload_service(self):
        return DocumentUploadService(
            document_repository=self.document_repository,
        )

    @cached_property
    def document_parser_service(self):
        return DocumentParserService()

    @cached_property
    def document_processing_service(self):
        return DocumentProcessingService(
            document_workflow_service=self.document_workflow_service,
            parser_service=self.document_parser_service,
            parsed_document_repository=self.parsed_document_repository,
        )

    @cached_property
    def document_chunker_service(self):
        return DocumentChunkerService()

    @cached_property
    def document_chunking_service(self):
        return DocumentChunkingService(
            document_chunk_repository=self.document_chunk_repository,
            parsed_document_repository=self.parsed_document_repository,
            document_workflow_service=self.document_workflow_service,
            document_chunker_service=self.document_chunker_service,
        )

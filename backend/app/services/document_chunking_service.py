from uuid import UUID

from app.core.logging import get_logger

from app.services.document_workflow_service import DocumentWorkflowService
from app.services.document_chunker_service import DocumentChunkerService

from app.models.document_chunk import DocumentChunk
from app.repositories.document_chunk_repository import DocumentChunkRepository
from app.repositories.parsed_document_repository import ParsedDocumentRepository


logger = get_logger(__name__)

class DocumentChunkingService:
    """
    Handles document parsing and persistence.
    """

    def __init__(
        self,
        document_chunk_repository: DocumentChunkRepository,
        parsed_document_repository: ParsedDocumentRepository,
        document_workflow_service: DocumentWorkflowService,
        document_chunker_service: DocumentChunkerService,
    ) -> None:
        self.document_chunk_repository = document_chunk_repository
        self.parsed_document_repository = parsed_document_repository
        self.document_workflow_service = document_workflow_service
        self.document_chunker_service = document_chunker_service

    async def chunk_document(
        self,
        document_id: UUID,
    ) -> list[DocumentChunk]:
        document = await self.document_workflow_service.get_document(
            document_id
        )
        if document is None:
            return []

        document = await self.document_workflow_service.begin_chunking(
            document
        )

        try:

            parsed_document = await self.parsed_document_repository.get_by_document_id(
                document_id
            )

            if parsed_document is None:
                await self.document_workflow_service.mark_chunking_failed(
                    document
                )
                return []

            document_chunks = await self.document_chunker_service.chunk(
                parsed_document
            )

            if not document_chunks:
                await self.document_workflow_service.mark_chunking_failed(
                    document
                )
                return []

            await self.document_workflow_service.mark_chunking_completed(
                document
            )

            return await self.document_chunk_repository.add_many(
                document_chunks
            )

        except Exception as e:
            document = await self.document_workflow_service.mark_chunking_failed(
                document
            )
            logger.exception(
                "Failed to chunk document %s",
                document_id,
            )
            raise

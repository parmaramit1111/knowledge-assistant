from uuid import UUID

from app.core.logging import get_logger

from app.services.document_workflow_service import DocumentWorkflowService

from app.models.document_chunk_embedding import DocumentChunkEmbedding
from app.repositories.document_chunk_repository import DocumentChunkRepository
from app.repositories.parsed_document_repository import ParsedDocumentRepository
from app.repositories.document_chunk_embedding_repository import DocumentChunkEmbeddingRepository
from app.services.document_embedder_service import DocumentEmbedderService


logger = get_logger(__name__)

class DocumentEmbeddingService:
    """
    Handles document parsing and persistence.
    """

    def __init__(
        self,
        document_chunk_repository: DocumentChunkRepository,
        parsed_document_repository: ParsedDocumentRepository,
        document_chunk_embedding_repository: DocumentChunkEmbeddingRepository,
        document_workflow_service: DocumentWorkflowService,
        document_embedder_service: DocumentEmbedderService,
    ) -> None:
        self.document_chunk_repository = document_chunk_repository
        self.parsed_document_repository = parsed_document_repository
        self.document_chunk_embedding_repository = document_chunk_embedding_repository
        self.document_workflow_service = document_workflow_service
        self.document_embedder_service = document_embedder_service

    async def embed_document(
        self,
        document_id: UUID,
    ) -> list[DocumentChunkEmbedding]:
        document = await self.document_workflow_service.get_document(
            document_id
        )
        if not document:
            return []

        parsed_document = await self.parsed_document_repository.get_by_document_id(
            document_id
        )
        if not parsed_document:
            await self.document_workflow_service.mark_embedding_failed(
                document
            )
            return []

        document_chunks = await self.document_chunk_repository.get_pending_embeddings(
            document_id=document_id,
            parsed_document_id=parsed_document.id
        )

        if not document_chunks:
            await self.document_workflow_service.mark_embedding_failed(
                document
            )
            return []

        await self.document_workflow_service.begin_embedding(
            document
        )

        try:
            document_chunk_embeddings: list[DocumentChunkEmbedding] = []
            for chunk in document_chunks:
                await self.document_chunk_repository.mark_embedding_running(
                    chunk
                )

                embedding_result = await self.document_embedder_service.embed(
                    chunk
                )
                document_chunk_embeddings.append(
                    DocumentChunkEmbedding(
                        document_chunk_id=chunk.id,
                        provider_name=embedding_result.provider_name,
                        provider_version=embedding_result.provider_version,
                        model_name=embedding_result.model_name,
                        dimensions=embedding_result.dimensions,
                        embedding=embedding_result.vector,
                        embedding_metadata=embedding_result.metadata or {},
                    )
                )

            saved_embeddings = await self.document_chunk_embedding_repository.add_many(
                document_chunk_embeddings
            )

            for chunk in document_chunks:
                await self.document_chunk_repository.mark_embedding_completed(
                    chunk
                )

            await self.document_workflow_service.mark_embedding_completed(
                document
            )
            return saved_embeddings
        except Exception:
            await self.document_workflow_service.mark_embedding_failed(
                document
            )
            for chunk in document_chunks:
                await self.document_chunk_repository.mark_embedding_failed(
                    chunk
                )
            logger.exception(
                "Failed to embed document %s",
                document_id,
            )
            raise

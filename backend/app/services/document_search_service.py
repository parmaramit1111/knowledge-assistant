from app.core.logging import get_logger

from app.repositories.document_chunk_embedding_repository import DocumentChunkEmbeddingRepository
from app.services.query_embedder_service import QueryEmbedderService
from app.schemas.search_request import SearchRequest
from app.schemas.search_response import SearchResponse, SearchResultItem

logger = get_logger(__name__)

class DocumentSearchService:
    """
    Service class for searching documents.
    """

    def __init__(
        self,
        document_chunk_embedding_repository: DocumentChunkEmbeddingRepository,
        query_embedder_service: QueryEmbedderService,
    ) -> None:
        self.document_chunk_embedding_repository = document_chunk_embedding_repository
        self.query_embedder_service = query_embedder_service

    async def search(
        self,
        search_request: SearchRequest,
    ) -> SearchResponse :
        logger.info(
            "Searching documents (top_k=%d)",
            search_request.top_k,
        )

        embedding_result = await self.query_embedder_service.embed_text(
            search_request.query
        )

        similar_chunks = await self.document_chunk_embedding_repository.similarity_search(
            query_embedding=embedding_result.vector,
            top_k=search_request.top_k,
        )

        results = [
            SearchResultItem(
                document_id=chunk.document_id,
                chunk_id=chunk.chunk_id,
                document_name=chunk.document_name,
                content=chunk.content,
                similarity_score=chunk.similarity_score,
                chunk_index=chunk.chunk_index,
            )
            for chunk in similar_chunks
        ]

        return SearchResponse(results=results)

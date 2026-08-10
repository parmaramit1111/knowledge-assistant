
from app.dtos.embedding_result import EmbeddingResult
from app.models.document_chunk import DocumentChunk
from app.providers.embeddings.factory import EmbeddingFactory

class DocumentEmbedderService:
    """
    Handles document embeding and persistence.
    """

    async def embed(
        self,
        document_chunk: DocumentChunk,
    ) -> EmbeddingResult:

        provider = EmbeddingFactory.get_embedding()

        vector = await provider.embed(document_chunk)
        return EmbeddingResult(
            vector=vector,
            provider_name=provider.name,
            provider_version=provider.version,
            model_name=provider.embedding_model,
            dimensions=provider.dimensions,
        )
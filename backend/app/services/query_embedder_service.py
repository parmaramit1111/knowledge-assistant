
from app.dtos.embedding_result import EmbeddingResult
from app.providers.embeddings.factory import EmbeddingFactory

class QueryEmbedderService:

    async def embed_text(
        self,
        question: str,
    ) -> EmbeddingResult:

        provider = EmbeddingFactory.get_embedding()

        vector = await provider.embed_text(question)

        return EmbeddingResult(
            vector=vector,
            provider_name=provider.name,
            provider_version=provider.version,
            model_name=provider.embedding_model,
            dimensions=provider.dimensions,
        )
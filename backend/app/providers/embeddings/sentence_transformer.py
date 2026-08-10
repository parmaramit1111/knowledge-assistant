from sentence_transformers import SentenceTransformer

from app.core.config import settings
from .base import BaseEmbedding
from app.models.document_chunk import DocumentChunk

class SentenceTransformerEmbedding(BaseEmbedding):

    @property
    def name(self) -> str:
        """Embedding name."""
        return settings.embedding_provider

    @property
    def version(self) -> str:
        """Embedding version."""
        return "1.0"

    @property
    def dimensions(self) -> int:
        return settings.embedding_dimension

    @property
    def embedding_model(self) -> str:
        return settings.embedding_model

    def __init__(self) -> None:
        print("SentenceTransformer initialized")
        self.model = SentenceTransformer(
            settings.embedding_model,
        )

    async def _embed(
        self,
        text: str,
    ) -> list[float]:
        """
        Generate an embedding vector for a document chunk.
        """

        embedding = self.model.encode(
            text,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

        return embedding.tolist()

    async def embed(
        self,
        document_chunk: DocumentChunk,
    ) -> list[float]:
        """
        Generate an embedding vector for a document chunk.
        """

        return await self._embed(document_chunk.content)

    async def embed_text(
        self,
        text: str,
    ) -> list[float]:
        """
        Generate an embedding vector for a document chunk.
        """
        return await self._embed(text)

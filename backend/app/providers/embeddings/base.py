from abc import ABC, abstractmethod

from app.models.document_chunk import DocumentChunk


class BaseEmbedding(ABC):
    """
    Generate a vector embedding for a document chunk.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Provider name."""
        ...

    @property
    @abstractmethod
    def version(self) -> str:
        """Provider version."""
        ...

    @property
    @abstractmethod
    def embedding_model(self) -> str:
        """Provider model."""
        ...

    @property
    @abstractmethod
    def dimensions(self) -> int:
        ...

    @abstractmethod
    async def embed(
        self,
        document_chunk: DocumentChunk,
    ) -> list[float]:
        """
        Generate an embedding vector for a document chunk.
        """
        ...
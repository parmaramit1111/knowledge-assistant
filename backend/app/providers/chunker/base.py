from abc import ABC, abstractmethod

from app.models.parsed_document import ParsedDocument
from app.models.document_chunk import DocumentChunk


class BaseChunker(ABC):
    """
    Base class for all document chunkers.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Chunker name."""
        ...

    @property
    @abstractmethod
    def version(self) -> str:
        """Chunker version."""
        ...

    @abstractmethod
    async def chunk(
        self,
        parsed_document: ParsedDocument,
    ) -> list[DocumentChunk]:
        """
        Split a parsed document into semantic chunks.
        """
        ...
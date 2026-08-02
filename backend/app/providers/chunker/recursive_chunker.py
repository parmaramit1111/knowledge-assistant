from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.core.config import settings
from .base import BaseChunker

from app.models.parsed_document import ParsedDocument
from app.models.document_chunk import DocumentChunk
from app.models.document import EmbeddingStatus

class RecursiveChunker(BaseChunker):

    @property
    def name(self) -> str:
        """Chunker name."""
        return "RecursiveCharacterTextSplitter"

    @property
    def version(self) -> str:
        """Chunker version."""
        return "1.0"

    def __init__(self):
        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap
        )

    async def chunk(
        self,
        parsed_document: ParsedDocument,
    ) -> list[DocumentChunk]:
        """
        Split a parsed document into semantic chunks.
        """
        content = parsed_document.content.strip()

        if not content:
            return []

        document_chunks: list[DocumentChunk] = []

        text_chunks = self._splitter.split_text(content)

        for chunk_index, text_chunk in enumerate(text_chunks):
            if not text_chunk.strip():
                continue

            document_chunk = DocumentChunk(
                document_id=parsed_document.document_id,
                parsed_document_id=parsed_document.id,
                chunk_index=chunk_index,
                content=text_chunk,
                character_count=len(text_chunk),
                token_count=0,
                chunk_metadata={
                    "chunker": self.name,
                    "version": self.version
                },
                embedding_status=EmbeddingStatus.PENDING,
            )

            document_chunks.append(document_chunk)

        return document_chunks
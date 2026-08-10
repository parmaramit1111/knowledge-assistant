from app.models.parsed_document import ParsedDocument
from app.models.document_chunk import DocumentChunk
from app.providers.chunker.factory import ChunkerFactory

class DocumentChunkerService:
    """
    Handles document parsing and persistence.
    """

    async def chunk(
        self,
        parsed_document: ParsedDocument,
    ) -> list[DocumentChunk]:

        chunker = ChunkerFactory.get_chunker()

        return await chunker.chunk(parsed_document)
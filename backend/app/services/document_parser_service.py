from __future__ import annotations
from app.models.document import Document
from app.models.parsed_document import ParsedDocument
from app.providers.parser.factory import ParserFactory
from app.repositories.parsed_document_repository import ParsedDocumentRepository

class DocumentParserService:
    """
    Handles document parsing and persistence.
    """

    def __init__(
        self,
        parsed_document_repository: ParsedDocumentRepository,
    ) -> None:
        self.parsed_document_repository = parsed_document_repository

    async def parse(
        self,
        document: Document,
    ) -> ParsedDocument:

        parser = ParserFactory.get_parser(
            document.content_type,
        )

        parsed_document = await parser.parse(
            document,
        )

        await self.parsed_document_repository.add(
            parsed_document,
        )

        return parsed_document
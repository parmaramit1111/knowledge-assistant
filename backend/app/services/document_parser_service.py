from app.models.document import Document
from app.models.parsed_document import ParsedDocument
from app.providers.parser.factory import ParserFactory


class DocumentParserService:
    """
    Handles document parsing and persistence.
    """

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

        return parsed_document
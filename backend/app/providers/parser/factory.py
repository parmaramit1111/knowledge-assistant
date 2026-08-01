from app.models.document import Document
from app.providers.parser.base import BaseParser
from app.providers.parser.pdf_parser import PdfParser


class ParserFactory:

    _parsers: list[type[BaseParser]] = [
        PdfParser,
        # DocxParser,
        # HtmlParser,
        # MarkdownParser,
        # TxtParser,
    ]

    @classmethod
    def get_parser(
        cls,
        content_type: str,
    ) -> BaseParser:

        for parser_class in cls._parsers:

            parser = parser_class()

            if content_type in parser.supported_content_types:
                return parser

        raise ValueError(
            f"No parser registered for '{content_type}'."
        )
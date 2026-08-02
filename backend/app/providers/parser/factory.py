from app.providers.parser.base import BaseParser
from app.providers.parser.pdf_parser import PdfParser
from app.providers.parser.text_parser import TextParser
from app.providers.parser.word_parser import WordParser
from app.providers.parser.markdown_parser import MarkdownParser
from app.providers.parser.html_parser import HtmlParser


class ParserFactory:

    _parsers: list[type[BaseParser]] = [
        PdfParser,
        TextParser,
        WordParser,
        MarkdownParser,
        HtmlParser,
    ]

    @classmethod
    def get_parser(
        cls,
        content_type: str,
    ) -> BaseParser:

        content_type = content_type.split(";", 1)[0].strip().lower()

        for parser_class in cls._parsers:

            parser = parser_class()

            if content_type in (
                mime.lower()
                for mime in parser.supported_content_types
            ):
                return parser

        raise ValueError(
            f"No parser registered for '{content_type}'."
        )
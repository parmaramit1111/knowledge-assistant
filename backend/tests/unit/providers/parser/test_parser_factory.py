
import pytest

from app.providers.parser.pdf_parser import PdfParser
from app.providers.parser.factory import ParserFactory

def test_returns_pdf_parser():

    parser = ParserFactory.get_parser(
        "application/pdf",
    )

    assert isinstance(parser, PdfParser)

def test_unknown_content_type():

    with pytest.raises(ValueError):

        ParserFactory.get_parser(
            "application/zip",
        )
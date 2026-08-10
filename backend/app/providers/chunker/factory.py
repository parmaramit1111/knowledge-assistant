from app.providers.chunker.base import BaseChunker
from app.providers.chunker.recursive_chunker import RecursiveChunker


class ChunkerFactory:
    """
    Factory responsible for resolving document chunkers.
    """

    _chunkers: list[type[BaseChunker]] = [
        RecursiveChunker,
    ]

    @classmethod
    def get_chunker(
        cls,
    ) -> BaseChunker:
        """
        Get the default document chunker.
        """
        return cls._chunkers[0]()
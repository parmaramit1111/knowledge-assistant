from app.providers.embeddings.base import BaseEmbedding


class EmbeddingFactory:
    """
    A factory for creating embedding providers.
    """

    _embeddings: list[type[BaseEmbedding]] = []
    _embedding: BaseEmbedding | None = None

    @classmethod
    def register(
        cls,
        provider: type[BaseEmbedding],
    ) -> None:
        cls._embeddings.append(provider)

    @classmethod
    def get_embedding(
        cls,
    ) -> BaseEmbedding:
        if cls._embedding is None:
            if not cls._embeddings:
                raise ValueError(
                    "No embedding provider registered."
                )

            cls._embedding = cls._embeddings[0]()

        return cls._embedding
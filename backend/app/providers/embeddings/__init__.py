from app.providers.embeddings.factory import EmbeddingFactory
from app.providers.embeddings.sentence_transformer import (
    SentenceTransformerEmbedding,
)

EmbeddingFactory.register(
    SentenceTransformerEmbedding,
)
from dataclasses import dataclass, field
from typing import Any

@dataclass(slots=True)
class EmbeddingResult:
    vector: list[float]
    provider_name: str
    provider_version: str
    model_name: str
    dimensions: int
    metadata: dict[str, Any] = field(default_factory=dict)
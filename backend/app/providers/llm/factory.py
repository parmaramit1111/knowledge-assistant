from app.core.config import settings

from .base import BaseLLM
from .ollama import OllamaProvider

class LLMFactory:

    @staticmethod
    def get_llm() -> BaseLLM:

        match settings.llm_provider:
            case "ollama":
                return OllamaProvider()

            case _:
                raise ValueError(
                    f"Unsupported LLM provider: {settings.llm_provider}"
                )
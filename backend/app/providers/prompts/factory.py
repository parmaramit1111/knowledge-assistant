from app.core.config import settings

from .base import BasePrompt
from .default_prompt import DefaultPrompt

class PromptFactory:

    @staticmethod
    def get_prompt() -> BasePrompt:
        match settings.prompt_provider:
            case "default":
                return DefaultPrompt()
            case _:
                raise ValueError(
                    f"Unsupported prompt provider: {settings.prompt_provider}"
                )
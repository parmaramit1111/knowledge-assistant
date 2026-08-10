from app.core.logging import get_logger

from app.models.chat_message import ChatMessage

from app.schemas.search_response import SearchResponse
from app.providers.prompts.factory import PromptFactory

logger = get_logger(__name__)

class PromptBuilderService:

    async def build(
        self,
        question: str,
        search_response: SearchResponse,
        chat_history: list[ChatMessage],
    ) -> str:

        provider = PromptFactory.get_prompt()

        logger.info(
            "Prompt Provider: %s (%s)",
            provider.name,
            provider.version,
        )

        return await provider.build(
            question,
            search_response,
            chat_history,
        )
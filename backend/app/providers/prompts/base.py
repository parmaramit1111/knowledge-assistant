from abc import ABC, abstractmethod

from app.models.chat_message import ChatMessage

from app.schemas.search_response import SearchResponse

class BasePrompt(ABC):

    @property
    def name(self) -> str:
        ...

    @property
    def version(self) -> str:
        ...

    @property
    def description(self) -> str:
        return "Default enterprise RAG prompt."

    @abstractmethod
    async def build(
        self,
        question: str,
        search_response: SearchResponse,
        chat_history: list[ChatMessage],
    ) -> str:
        ...
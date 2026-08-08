from app.core.logging import get_logger

from app.core.config import settings
from app.services.document_search_service import DocumentSearchService
from app.services.prompt_builder_service import PromptBuilderService
from app.services.llm_service import LLMService

from app.schemas.chat_request import ChatRequest
from app.schemas.chat_response import ChatResponse, SourceItem

from app.schemas.search_request import SearchRequest

logger = get_logger(__name__)

class DocumentChatService:

    def __init__(
        self,
        document_search_service: DocumentSearchService,
        prompt_builder_service: PromptBuilderService,
        llm_service: LLMService,
    ) -> None:
        self.document_search_service = document_search_service
        self.prompt_builder_service = prompt_builder_service
        self.llm_service = llm_service

    async def ask(
        self,
        chat_request: ChatRequest,
    ) -> ChatResponse :
        logger.info(
            "Question: %s",
            chat_request.question,
        )
        sources: list[SourceItem] = []

        search_request = SearchRequest(
            query=chat_request.question,
            top_k=settings.search_top_k,
        )

        search_result = await self.document_search_service.search(
            search_request
        )
        if not search_result.results:
            return ChatResponse(
                answer="I cannot find the answer in the provided documents.",
                sources=[],
            )

        sources = [
            SourceItem(
                document_name=item.document_name,
                chunk_index=item.chunk_index,
            )
            for item in search_result.results
        ]

        prompt_result = await self.prompt_builder_service.build(
            question=chat_request.question,
            search_response=search_result,
        )

        llm_result = await self.llm_service.generate(prompt_result)

        return ChatResponse(
            answer=llm_result,
            sources=sources,
        )

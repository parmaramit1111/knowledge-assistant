from uuid import uuid4

from app.core.logging import get_logger

from app.core.config import settings
from app.services.document_search_service import DocumentSearchService
from app.services.prompt_builder_service import PromptBuilderService
from app.services.llm_service import LLMService
from app.services.chat_history_service import ChatHistoryService

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
        chat_history_service: ChatHistoryService,
    ) -> None:
        self.document_search_service = document_search_service
        self.prompt_builder_service = prompt_builder_service
        self.llm_service = llm_service
        self.chat_history_service = chat_history_service

    async def ask(
        self,
        chat_request: ChatRequest,
    ) -> ChatResponse :
        logger.info(
            "Question: %s",
            chat_request.question,
        )
        sources: list[SourceItem] = []

        conversation_id = chat_request.conversation_id or uuid4()

        chat_history = await self.chat_history_service.get_history(
            conversation_id=conversation_id,
        )

        await self.chat_history_service.add_user_message(
            conversation_id=conversation_id,
            content=chat_request.question,
        )

        search_request = SearchRequest(
            query=chat_request.question,
            top_k=settings.search_top_k,
        )

        search_result = await self.document_search_service.search(
            search_request
        )

        if not search_result.results:
            answer = "I cannot find the answer in the provided documents."

            await self.chat_history_service.add_assistant_message(
                conversation_id=conversation_id,
                content=answer,
            )

            return ChatResponse(
                conversation_id=conversation_id,
                answer=answer,
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
            chat_history=chat_history,
        )

        llm_result = await self.llm_service.generate(prompt_result)

        await self.chat_history_service.add_assistant_message(
            conversation_id=conversation_id,
            content=llm_result,
        )

        return ChatResponse(
            conversation_id=conversation_id,
            answer=llm_result,
            sources=sources,
        )

from uuid import UUID

from app.models.chat_message import ChatMessage, Roles
from app.repositories.chat_message_repository import ChatMessageRepository

class ChatHistoryService:

    def __init__(
        self,
        chat_message_repository: ChatMessageRepository,
    ) -> None:
        self.chat_message_repository = chat_message_repository

    async def add_user_message(
        self,
        conversation_id: UUID,
        content: str,
    ) -> ChatMessage:
        return await self.chat_message_repository.add_message(
            conversation_id=conversation_id,
            role=Roles.USER,
            content=content,
        )

    async def add_assistant_message(
        self,
        conversation_id: UUID,
        content: str,
    ) -> ChatMessage:
        return await self.chat_message_repository.add_message(
            conversation_id=conversation_id,
            role=Roles.ASSISTANT,
            content=content,
        )

    async def get_history(
        self,
        conversation_id: UUID,
    ) -> list[ChatMessage]:
        return await self.chat_message_repository.get_history(
            conversation_id=conversation_id
        )
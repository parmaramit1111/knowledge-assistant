from uuid import UUID
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.chat_message import ChatMessage, Roles
from .base import BaseRepository

class ChatMessageRepository(BaseRepository[ChatMessage]):
    def __init__(
        self,
        session: AsyncSession,
    ):
        super().__init__(
            session,
            ChatMessage
        )

    async def add_message(
        self,
        conversation_id: UUID,
        role: Roles,
        content: str,
    ) -> ChatMessage:
        return await self.add(
            ChatMessage(
                conversation_id=conversation_id,
                role=role,
                content=content,
            )
        )

    async def get_history(
        self,
        conversation_id: UUID,
    ) -> list[ChatMessage]:
        return await self.find(
            ChatMessage.conversation_id==conversation_id,
            limit=10,
            order_by=desc(ChatMessage.created_at),
        )
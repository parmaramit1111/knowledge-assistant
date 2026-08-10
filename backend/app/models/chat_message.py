from enum import Enum
from uuid import UUID

from sqlalchemy import Text, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseEntity


class Roles(str, Enum):
    USER = "USER"
    ASSISTANT = "ASSISTANT"


class ChatMessage(BaseEntity):
    __tablename__ = "chat_messages"

    conversation_id: Mapped[UUID] = mapped_column(
        index=True,
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    role: Mapped[Roles] = mapped_column(
        SqlEnum(
            Roles,
            name="roles",
        ),
        nullable=False,
        default=Roles.USER,
    )
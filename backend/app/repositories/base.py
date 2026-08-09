from typing import Generic, TypeVar
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

from app.models.base import BaseEntity

T = TypeVar("T", bound=BaseEntity)


class BaseRepository(Generic[T]):
    """
    Generic repository providing common CRUD operations.
    """

    def __init__(
        self,
        session: AsyncSession,
        model: type[T],
    ) -> None:
        self._session = session
        self._model = model

    async def add(self, entity: T) -> T:
        self._session.add(entity)
        await self._session.flush()
        await self._session.refresh(entity)
        return entity

    async def add_many(self, entities: list[T]) -> list[T]:
        self._session.add_all(entities)
        await self._session.flush()

        for entity in entities:
            await self._session.refresh(entity)

        return entities

    async def update(self, entity: T) -> T:
        await self._session.flush()
        await self._session.refresh(entity)
        return entity

    async def delete(self, entity: T) -> None:
        await self._session.delete(entity)

    async def get_by_id(self, id: UUID) -> T | None:
        statement = (
            select(self._model)
            .where(self._model.id == id)
        )

        result = await self._session.execute(statement)

        return result.scalar_one_or_none()

    async def find(
        self,
        *conditions,
        limit: int | None = None,
        offset: int | None = None,
        order_by=None,
    ) -> list[T]:
        statement = (
            select(self._model)
            .where(*conditions)
        )

        if order_by is not None:
            statement = statement.order_by(order_by)

        if offset is not None:
            statement = statement.offset(offset)

        if limit is not None:
            statement = statement.limit(limit)

        result = await self._session.execute(statement)

        return list(result.scalars().all())

    async def find_one(self, *conditions,) -> T | None:
        statement = (
            select(self._model)
                .where(*conditions)
                .limit(1)
        )

        result = await self._session.execute(statement)

        return result.scalars().one_or_none()

    async def get_all(self) -> list[T]:
        statement = select(self._model)

        result = await self._session.execute(statement)

        return list(result.scalars().all())

    async def exists(self, id: UUID) -> bool:
        statement = (
            select(func.count())
            .select_from(self._model)
            .where(self._model.id == id)
        )

        result = await self._session.execute(statement)

        return result.scalar_one() > 0

    async def count(self) -> int:
        statement = (
            select(func.count())
            .select_from(self._model)
        )

        result = await self._session.execute(statement)

        return result.scalar_one()

    async def flush(self) -> None:
        await self._session.flush()

    async def refresh(self, entity: T) -> None:
        await self._session.refresh(entity)
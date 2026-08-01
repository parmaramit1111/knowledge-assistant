from functools import wraps
from typing import Any, Callable, Awaitable

from app.core.database import AsyncSessionLocal
from app.core.transaction.context import (
    set_session,
    reset_session,
)


def transactional(
    func: Callable[..., Awaitable[Any]],
) -> Callable[..., Awaitable[Any]]:
    """
    Decorator that executes a command inside a database transaction.
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):

        async with AsyncSessionLocal() as session:

            token = set_session(session)

            try:
                result = await func(*args, **kwargs)

                await session.commit()

                return result

            except Exception:

                await session.rollback()

                raise

            finally:

                reset_session(token)

    return wrapper
from contextvars import ContextVar

from sqlalchemy.ext.asyncio import AsyncSession


_session_context: ContextVar[AsyncSession | None] = ContextVar(
    "db_session",
    default=None,
)


def set_session(session: AsyncSession):
    """
    Store the current database session in the request context.
    """
    return _session_context.set(session)


def get_session() -> AsyncSession:
    """
    Get the current active database session.

    Raises:
        RuntimeError: If no active transaction exists.
    """
    session = _session_context.get()

    if session is None:
        raise RuntimeError(
            "No active database transaction. "
            "Did you forget to decorate the command with @transactional?"
        )

    return session


def reset_session(token) -> None:
    """
    Remove the current database session from the context.
    """
    _session_context.reset(token)
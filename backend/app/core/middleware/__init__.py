from fastapi import FastAPI
from .request_id import RequestIdMiddleware

__all__ = [
    "register_middlewares",
    "RequestIdMiddleware",
]

def register_middlewares(app: FastAPI) -> None:
    """Register all application middlewares.

    Note:
        Starlette executes middlewares in reverse order of registration.
    """

    app.add_middleware(RequestIdMiddleware)

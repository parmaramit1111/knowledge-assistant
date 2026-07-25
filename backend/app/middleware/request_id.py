import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint
from starlette.responses import Response
from starlette.requests import Request
from app.core.logging import request_id_context

REQUEST_ID_HEADER = "X-Request-ID"

class RequestIdMiddleware(BaseHTTPMiddleware):
    """
    Middleware that ensures every request has
    a unique correlation identifier.

    The identifier is stored in a ContextVar
    and added to the response headers.
    """

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """
        Process incoming requests and generate a unique ID if one is not present.

        Args:
            request: The incoming HTTP request.
            call_next: The next middleware or route handler in the chain.

        Returns:
            The HTTP response.

        Note:
            If a request ID is already present in the request headers,
            it will be used instead of generating a new one.
        """
        request_id = request.headers.get(REQUEST_ID_HEADER) or str(uuid.uuid4())
        token = request_id_context.set(request_id)

        # Make it available downstream
        request.state.request_id = request_id

        try:
            response = await call_next(request)
            response.headers[REQUEST_ID_HEADER] = request_id
            return response
        finally:
            request_id_context.reset(token)

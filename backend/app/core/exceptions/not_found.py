from typing import Optional, Any
from http import HTTPStatus
from .base import AppException
from app.schemas.api_response import ResponseCode

class ResourceNotFoundException(AppException):
    """Exception raised when a resource is not found."""

    STATUS: HTTPStatus = HTTPStatus.NOT_FOUND

    def __init__(self, detail: str = "Resource not found", *, extra: Optional[dict[str, Any]] = None) -> None:
        super().__init__(
            status_code=self.STATUS,
            detail=detail,
            code=ResponseCode.NOT_FOUND,
            extra=extra
        )

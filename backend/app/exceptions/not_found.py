from typing import Optional, Any
from http import HTTPStatus
from .base import AppException

class ResourceNotFoundException(AppException):
    """Exception raised when a resource is not found."""

    STATUS: HTTPStatus = HTTPStatus.NOT_FOUND
    CODE: str = "NOT_FOUND"

    def __init__(self, detail: str = "Resource not found", *, extra: Optional[dict[str, Any]] = None) -> None:
        super().__init__(
            status_code=self.STATUS,
            detail=detail,
            code=self.CODE,
            extra=extra
        )

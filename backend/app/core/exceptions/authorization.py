from typing import Optional, Any
from http import HTTPStatus
from .base import AppException
from app.schemas.api_response import ResponseCode

class UnauthorizedException(AppException):
    STATUS: HTTPStatus = HTTPStatus.UNAUTHORIZED

    def __init__(self, detail: str = "Not authenticated", *, extra: Optional[dict[str, Any]] = None) -> None:
        super().__init__(
            status_code=self.STATUS,
            detail=detail,
            code=ResponseCode.UNAUTHORIZED,
            extra=extra
        )

class ForbiddenException(AppException):

    STATUS: HTTPStatus = HTTPStatus.FORBIDDEN
    def __init__(self, detail: str = "Not enough permissions", *, extra: Optional[dict[str, Any]] = None) -> None:
        super().__init__(
            status_code=self.STATUS,
            detail=detail,
            code=ResponseCode.FORBIDDEN,
            extra=extra
        )

from typing import Optional, Any
from http import HTTPStatus
from .base import AppException

class UnauthorizedException(AppException):
    STATUS: HTTPStatus = HTTPStatus.UNAUTHORIZED
    CODE: str = "UNAUTHORIZED"

    def __init__(self, detail: str = "Not authenticated", *, extra: Optional[dict[str, Any]] = None) -> None:
        super().__init__(
            status_code=self.STATUS,
            detail=detail,
            code=self.CODE,
            extra=extra
        )

class ForbiddenException(AppException):

    STATUS: HTTPStatus = HTTPStatus.FORBIDDEN
    CODE: str = "FORBIDDEN"
    def __init__(self, detail: str = "Not enough permissions", *, extra: Optional[dict[str, Any]] = None) -> None:
        super().__init__(
            status_code=self.STATUS,
            detail=detail,
            code=self.CODE, extra=extra
        )

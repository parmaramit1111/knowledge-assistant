from enum import Enum
from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict

T = TypeVar("T")

class ResponseCode(str, Enum):
    SUCCESS = "SUCCESS"

    VALIDATION_ERROR = "VALIDATION_ERROR"
    INVALID_INPUT = "INVALID_INPUT"

    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN"

    NOT_FOUND = "NOT_FOUND"
    CONFLICT = "CONFLICT"

    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"


class ApiResponse(BaseModel, Generic[T]):
    model_config = ConfigDict(from_attributes=True)

    code: ResponseCode
    success: bool
    message: str

    result: T | None = None

    total_records: int | None = None

    request_id: str | None = None
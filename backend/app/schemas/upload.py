from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UploadResponse(BaseModel):
    id: UUID
    filename: str
    size: int
    content_type: str
    uploaded_at: datetime
    message: str
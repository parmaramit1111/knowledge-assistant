from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

class UploadResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID

    filename: str

    content_type: str

    size: int

    message: str = "Document uploaded successfully."

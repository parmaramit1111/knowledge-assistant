from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

class UploadResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID

    filename: str

    content_type: str

    size: int

    uploaded_at: datetime

    message: str = "Document uploaded successfully."

class IngestionRequest(BaseModel):
    pass

class IngestionResponse(BaseModel):
    pass
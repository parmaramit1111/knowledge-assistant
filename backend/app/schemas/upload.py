from datetime import UTC, datetime
from pathlib import Path
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class UploadResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID

    filename: str
    original_filename: str

    content_type: str
    size: int

    uploaded_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    storage_path: Path

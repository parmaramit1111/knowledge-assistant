from fastapi import UploadFile
from pydantic import BaseModel, ConfigDict


class UploadDocumentCommand(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    file: UploadFile
from fastapi import APIRouter, Depends, File, UploadFile, status

from app.commands.upload.upload_document import UploadDocumentCommand
from app.api.dependencies import get_document_upload_service
from app.schemas.upload import UploadResponse
from app.services.document_upload_service import DocumentUploadService

from .docs import (
    UPLOAD_DESCRIPTION,
    UPLOAD_SUCCESS_DESCRIPTION,
    UPLOAD_SUMMARY,
)

router = APIRouter()


@router.post(
    "/upload",
    response_model=UploadResponse,
    status_code=status.HTTP_201_CREATED,
    summary=UPLOAD_SUMMARY,
    description=UPLOAD_DESCRIPTION,
    responses={
        status.HTTP_201_CREATED: {
            "description": UPLOAD_SUCCESS_DESCRIPTION,
        }
    },
)
async def upload_document(
    file: UploadFile = File(...),
    service: DocumentUploadService = Depends(get_document_upload_service),
) -> UploadResponse:
    command = UploadDocumentCommand(file=file)

    document = await service.execute(command)

    return UploadResponse.model_validate(document)
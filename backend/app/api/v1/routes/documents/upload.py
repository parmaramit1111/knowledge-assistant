from fastapi import APIRouter, File, UploadFile, status

from app.commands.upload.upload_document import UploadDocumentCommand
from app.schemas.api_response import ApiResponse
from app.schemas.document import UploadResponse
from app.schemas.response_factory import ResponseFactory

from .docs import (
    UPLOAD_DESCRIPTION,
    UPLOAD_SUCCESS_DESCRIPTION,
    UPLOAD_SUMMARY,
)

router = APIRouter()


@router.post(
    "/upload",
    response_model=ApiResponse[UploadResponse],
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
) -> ApiResponse[UploadResponse]:
    command = UploadDocumentCommand(
        file=file,
    )

    document = await command.execute()

    return ResponseFactory.success(
        result=UploadResponse.model_validate(document),
        message="Document uploaded successfully.",
    )
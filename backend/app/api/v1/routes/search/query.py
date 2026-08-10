from fastapi import APIRouter, status

from app.core.execution.context import ExecutionContext
from app.queries.search.search_documents_query import SearchDocumentsQuery
from app.schemas.api_response import ApiResponse
from app.schemas.search_request import SearchRequest
from app.schemas.search_response import SearchResponse
from app.schemas.response_factory import ResponseFactory

from .docs import (
    QUERY_DESCRIPTION,
    QUERY_SUCCESS_DESCRIPTION,
    QUERY_SUMMARY,
)

router = APIRouter()


@router.post(
    "/query",
    response_model=ApiResponse[SearchResponse],
    status_code=status.HTTP_200_OK,
    summary=QUERY_SUMMARY,
    description=QUERY_DESCRIPTION,
    responses={
        status.HTTP_200_OK: {
            "description": QUERY_SUCCESS_DESCRIPTION,
        }
    },
)
async def search_query(
    search_request: SearchRequest,
) -> ApiResponse[SearchResponse]:

    async with ExecutionContext() as context:
        query = SearchDocumentsQuery(context.document_search_service)

        search_result = await query.execute(search_request)

        return ResponseFactory.success(
            result=SearchResponse.model_validate(search_result),
            message="Search completed successfully.",
        )
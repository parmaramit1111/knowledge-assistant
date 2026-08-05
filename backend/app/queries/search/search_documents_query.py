from app.core.logging import get_logger

from app.schemas.search_request import SearchRequest
from app.services.document_search_service import DocumentSearchService


logger = get_logger(__name__)

class SearchDocumentsQuery:
    def __init__(
        self,
        document_search_service: DocumentSearchService,
    ) -> None:
        self.document_search_service = document_search_service

    async def execute(self, search_request: SearchRequest,):
        return await self.document_search_service.search(
            search_request
        )

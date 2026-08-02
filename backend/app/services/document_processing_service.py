from uuid import UUID

from app.core.logging import get_logger

from app.services.document_workflow_service import DocumentWorkflowService
from app.services.document_parser_service import DocumentParserService
from app.repositories.parsed_document_repository import ParsedDocumentRepository

logger = get_logger(__name__)

class DocumentProcessingService:

    def __init__(
        self,
        document_workflow_service: DocumentWorkflowService,
        parser_service: DocumentParserService,
        parsed_document_repository: ParsedDocumentRepository,
    ) -> None:
        self.document_workflow_service = document_workflow_service
        self.parser_service =  parser_service
        self.parsed_document_repository = parsed_document_repository

    async def process_document(
        self,
        document_id: UUID,
    ) -> None:
        document = await self.document_workflow_service.get_document(document_id)

        if document is None:
            return

        await self.document_workflow_service.begin_processing(document_id)

        try:
            parsed_document = await self.parser_service.parse(document)

            parsed_document = await self.parsed_document_repository.add(
                parsed_document
            )

            await self.document_workflow_service.mark_parsing_completed(document)
        except Exception:
            await self.document_workflow_service.mark_parsing_failed(document)
            logger.exception(
                "Failed to parse document %s",
                document_id,
            )
            raise
        # document = await self.begin_processing(document_id)

        # if document is None:
        #     return

        # try:
        #     await self.parser_service.parse(document)

        #     await self.mark_parsing_completed(
        #         document,
        #     )
        # except Exception:
        #     await self.mark_parsing_failed(
        #         document,
        #     )
        #     raise
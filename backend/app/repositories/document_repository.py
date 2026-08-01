from .base import BaseRepository
from app.models.document import Document

class DocumentRepository(BaseRepository[Document]):

    def __init__(self):
        super().__init__(Document)
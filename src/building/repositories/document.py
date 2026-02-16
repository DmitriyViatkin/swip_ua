from .base import BaseRepository
from src.building.models.document import Document


class DocumentRepository(BaseRepository[Document]):
    def __init__(self):
        super().__init__(Document)

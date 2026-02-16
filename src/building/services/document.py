from src.building.services.base import BaseService
from src.building.repositories.document import DocumentRepository
from src.building.models.document import Document


class DocumentService(BaseService[Document]):
    def __init__(self):
        super().__init__(DocumentRepository())
from src.building.services.base import BaseService
from src.building.repositories.section import SectionRepository
from src.building.models.section import Section


class SectionService(BaseService[Section]):
    def __init__(self):
        super().__init__(SectionRepository())
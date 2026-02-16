from .base import BaseRepository
from src.building.models.section import Section


class SectionRepository(BaseRepository[Section]):
    def __init__(self):
        super().__init__(Section)
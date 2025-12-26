from .base import BaseRepository
from src.building.models.flat import Flat


class FlatRepository(BaseRepository[Flat]):
    def __init__(self):
        super().__init__(Flat)
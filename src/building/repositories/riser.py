from .base import BaseRepository
from src.building.models.riser import Riser


class RiserRepository(BaseRepository[Riser]):
    def __init__(self):
        super().__init__(Riser)
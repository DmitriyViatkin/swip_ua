from .base import BaseRepository
from src.building.models.floor import Floor


class FloorRepository(BaseRepository[Floor]):
    def __init__(self):
        super().__init__(Floor)

        
from .base import BaseRepository
from src.building.models.corps import Corps


class CorpsRepository(BaseRepository[Corps]):
    def __init__(self):
        super().__init__(Corps)
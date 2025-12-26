from .base import BaseRepository
from src.building.models.advantage_of_home import Advantages_of_Home


class AdvantagesOfHomeRepository(BaseRepository[Advantages_of_Home]):
    def __init__(self):
        super().__init__(Advantages_of_Home)
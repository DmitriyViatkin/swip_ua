from src.building.services.base import BaseService
from src.building.repositories.floor import FloorRepository
from src.building.models.floor import Floor


class FloorService(BaseService[Floor]):
    def __init__(self):
        super().__init__(FloorRepository())

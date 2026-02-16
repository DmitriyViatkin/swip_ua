from src.building.services.base import BaseService
from src.building.repositories.corps import CorpsRepository
from src.building.models.corps import Corps


class CorpsService(BaseService[Corps]):
    def __init__(self):
        super().__init__(CorpsRepository())

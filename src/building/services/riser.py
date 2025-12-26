from src.building.services.base import BaseService
from src.building.repositories.riser import RiserRepository
from src.building.models.riser import Riser


class RiserService(BaseService[Riser]):
    def __init__(self):
        super().__init__(RiserRepository())
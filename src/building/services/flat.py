from src.building.services.base import BaseService
from src.building.repositories.flat import FlatRepository
from src.building.models.flat import Flat


class FlatService(BaseService[Flat]):
    def __init__(self):
        super().__init__(FlatRepository())
from src.building.services.base import BaseService
from src.building.repositories.advantages_of_home import AdvantagesOfHomeRepository
from src.building.models.advantage_of_home import Advantages_of_Home


class AdvantagesOfHomeService(BaseService[Advantages_of_Home]):
    def __init__(self):
        super().__init__(AdvantagesOfHomeRepository())
from .base import BaseRepository
from src.building.models.registration_and_payment import Registration_and_Payment


class RegistrationAndPaymentRepository(BaseRepository[Registration_and_Payment]):
    def __init__(self):
        super().__init__(Registration_and_Payment)
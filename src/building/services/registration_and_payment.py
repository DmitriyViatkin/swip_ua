from src.building.services.base import BaseService
from src.building.repositories.registration_and_payment import RegistrationAndPaymentRepository
from src.building.models.registration_and_payment import Registration_and_Payment


class RegistrationAndPaymentService(BaseService[Registration_and_Payment]):
    def __init__(self):
        super().__init__(RegistrationAndPaymentRepository())

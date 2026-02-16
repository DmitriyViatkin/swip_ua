from pydantic import BaseModel
from decimal import Decimal


class RegistrationPaymentBase(BaseModel):
    registration: str | None = None
    options: str | None = None
    appointment: str | None = None
    price: Decimal | None = None


class RegistrationPaymentCreate(RegistrationPaymentBase):
    house_id: int


class RegistrationPaymentRead(RegistrationPaymentBase):
    id: int
    house_id: int

    model_config = {"from_attributes": True}
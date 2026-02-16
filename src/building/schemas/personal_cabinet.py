from pydantic import BaseModel, EmailStr, Field, ConfigDict
from src.users.schemas.user.user_read import UserRead
from .news import NewsRead
from .infrastructure import InfrastructureRead
from .document import DocumentRead
from  .registration_and_payment import RegistrationPaymentRead
from typing import Optional, List
from .house import HouseRead


class PersonalCabinet(BaseModel):
    user: UserRead
    house: Optional[HouseRead] = None

    news: List[NewsRead] = []
    document: List[DocumentRead] = []

    infrastructure: Optional[InfrastructureRead] = None
    registration_payment: Optional[RegistrationPaymentRead] = None

    model_config = {"from_attributes": True}



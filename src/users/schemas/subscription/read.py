from datetime import datetime
from .base import SubscriptionBase
from pydantic import BaseModel, EmailStr, Field, ConfigDict

class SubscriptionRead(SubscriptionBase):
    id: int
    date: datetime

    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True
    )
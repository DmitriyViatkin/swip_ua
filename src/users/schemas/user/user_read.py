
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from .user_base import UserBase
from src.users.schemas.subscription.read import SubscriptionRead
from src.users.schemas.notification.read import NotificationRead
from typing import Optional



class UserRead(UserBase):
    id: int
    date: datetime
    subscription: Optional[SubscriptionRead] = None
    notification: Optional[NotificationRead] = None

    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True
    )
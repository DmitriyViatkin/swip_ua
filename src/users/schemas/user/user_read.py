
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from .user_base import UserBase
from .agent import UserAgentRead
from src.users.schemas.subscription.read import SubscriptionRead
from src.users.schemas.notification.read import NotificationRead
from src.users.schemas.redirections.read import RedirectionRead

from typing import Optional, List


class UserRead(UserBase):
    id: int
    date: datetime

    subscription: Optional[SubscriptionRead] = None
    notification: Optional[NotificationRead] = None
    redirection: Optional[RedirectionRead] = None
    photo: Optional[str]
    agent: Optional[UserAgentRead] = None
    clients: Optional[List["UserRead"]] = None

    model_config = {
        "from_attributes": True
    }
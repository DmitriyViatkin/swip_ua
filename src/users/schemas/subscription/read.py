from datetime import datetime
from .base import SubscriptionBase


class SubscriptionRead(SubscriptionBase):
    id: int
    date: datetime

    class Config:
        orm_mode = True
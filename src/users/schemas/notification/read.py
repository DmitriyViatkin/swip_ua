from datetime import datetime
from .base import NotificationBase


class NotificationRead(NotificationBase):
    id: int

    class Config:
        orm_mode = True
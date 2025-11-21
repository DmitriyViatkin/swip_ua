from datetime import datetime
from .base import RedirectionBase


class RedirectionRead(RedirectionBase):
    id: int
    date: datetime

    class Config:
        orm_mode = True
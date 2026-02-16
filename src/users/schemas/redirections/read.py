from datetime import datetime
from pydantic import ConfigDict
from .base import RedirectionBase


class RedirectionRead(RedirectionBase):
    id: int
    date: datetime

    model_config = ConfigDict(from_attributes=True)
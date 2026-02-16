from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional, ForwardRef



from datetime import datetime
from .base import NotificationBase


class NotificationRead(NotificationBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )

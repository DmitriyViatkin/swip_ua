from pydantic import BaseModel
from typing import Optional


class NotificationUpdate(BaseModel):
    client_id: Optional[int] = None
    agent_id: Optional[int] = None

    is_me: Optional[bool] = None
    is_me_agent: Optional[bool] = None
    is_agent: Optional[bool] = None
    turn_off: Optional[bool] = None
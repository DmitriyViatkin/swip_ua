from pydantic import BaseModel
from typing import Optional


class NotificationBase(BaseModel):
    client_id: Optional[int] = None
    agent_id: Optional[int] = None

    is_me: bool = False
    is_me_agent: bool = False
    is_agent: bool = False
    turn_off: bool = False
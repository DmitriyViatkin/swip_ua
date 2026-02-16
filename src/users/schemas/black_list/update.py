from pydantic import BaseModel
from typing import Optional


class BlackListUpdate(BaseModel):
    user_id: Optional[int] = None
from pydantic import BaseModel
from typing import Optional


class RedirectionBase(BaseModel):
    user_id: Optional[int] = None
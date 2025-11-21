from pydantic import BaseModel
from typing import Optional


class RedirectionUpdate(BaseModel):
    user_id: Optional[int] = None
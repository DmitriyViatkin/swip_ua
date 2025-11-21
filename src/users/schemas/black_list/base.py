from pydantic import BaseModel
from typing import Optional


class BlackListBase(BaseModel):
    user_id: Optional[int] = None
from pydantic import BaseModel
from typing import Optional


class SubscriptionBase(BaseModel):
    user_id: Optional[int] = None
    auto_renewal: bool = True
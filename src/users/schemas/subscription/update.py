from pydantic import BaseModel
from typing import Optional


class SubscriptionUpdate(BaseModel):
    user_id: Optional[int] = None
    auto_renewal: Optional[bool] = None
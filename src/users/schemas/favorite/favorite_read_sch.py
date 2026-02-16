from .favorite_base_sch import FavoriteBase
from pydantic import  ConfigDict, BaseModel
from typing import List
from datetime import datetime

class FavoriteRead(FavoriteBase):

    id: int
    user_id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class FavoriteList(BaseModel):
    items: List[FavoriteRead]
    model_config = ConfigDict(from_attributes=True)


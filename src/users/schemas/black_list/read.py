from .base import BlackListBase
from pydantic import BaseModel, ConfigDict
from typing import List
class BlackListRead(BlackListBase):
    id: int
    first_name: str
    last_name: str
    email: str

    model_config = ConfigDict(from_attributes=True)

class UserBlackList(BaseModel):
    items: List[BlackListRead]
    model_config = ConfigDict(from_attributes=True)


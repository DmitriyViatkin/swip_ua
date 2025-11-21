from datetime import datetime
from .user_base import UserBase

class UserRead(UserBase):
    id: int
    date: datetime

    class Config:
        orm_mode = True
        use_enum_values = True
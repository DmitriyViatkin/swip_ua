
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from .user_base import UserBase

class UserRead(UserBase):
    id: int
    date: datetime


    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True
    )
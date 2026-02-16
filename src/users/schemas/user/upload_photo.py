
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from .user_base import UserBase
from typing import Optional


class UserRead(UserBase):
    id: int
    photo: Optional[str] = None
from typing import Optional
from pydantic import BaseModel, Field,ConfigDict
from src.enums import UserRole

class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    phone: Optional[str] = Field(None, max_length=20)
    role: Optional[UserRole] = None
    photo: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
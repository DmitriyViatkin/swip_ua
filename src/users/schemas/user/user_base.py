from pydantic import BaseModel, EmailStr, Field
from src.enums import UserRole
from typing import Optional

class UserBase(BaseModel):
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = UserRole.CLIENT

    class Config:
        orm_mode = True
        use_enum_values = True
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from src.enums import UserRole
from typing import Optional
#from src.users.schemas.notification.base import NotificationBase

class UserBase(BaseModel):
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    role: UserRole = UserRole.CLIENT
   # notification: "NotificationBase"

    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True
    )
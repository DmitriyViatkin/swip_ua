from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from src.enums import UserRole

class UserLoginRead(BaseModel):
    id: int
    email: EmailStr
    role: str
    photo: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
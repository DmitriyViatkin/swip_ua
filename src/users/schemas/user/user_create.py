from pydantic import EmailStr
from .user_base import UserBase
from src.enums import UserRole

class UserCreateSchema(UserBase):
    first_name: str
    last_name: str
    phone: str
    email: str
    password: str
    role: UserRole = UserRole.CLIENT
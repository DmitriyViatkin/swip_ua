from pydantic import EmailStr
from .user_base import UserBase

class UserCreateSchema(UserBase):
    email: EmailStr
    first_name: str
    last_name: str
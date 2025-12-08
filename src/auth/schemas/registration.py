from pydantic import BaseModel, EmailStr, constr
from src.enums import UserRole
from typing import Optional

class UserRegister(BaseModel):
    first_name: constr(min_length=1, max_length=50)
    last_name: constr(min_length=1, max_length=50)
    phone: constr(min_length=5, max_length=20)
    email: EmailStr
    password: constr(min_length=8, max_length=128)
    role: UserRole = UserRole.client
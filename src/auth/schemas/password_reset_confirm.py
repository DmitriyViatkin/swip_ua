from pydantic import BaseModel, EmailStr

 

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str
from pydantic import BaseModel, EmailStr

class VerifyRequest(BaseModel):
    email: EmailStr
    code: str
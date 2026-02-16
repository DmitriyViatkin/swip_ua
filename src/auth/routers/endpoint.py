from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel,EmailStr
from dishka.integrations.fastapi import FromDishka, inject
from src.auth.services.auth_service import AuthService

router = APIRouter()


class LoginRequest(BaseModel):
    username: EmailStr
    password: str


@router.post("/login")
@inject
async def login(
        request: LoginRequest,
        service: FromDishka[AuthService],
):
    user = await service.authenticate(request.username, request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    tokens = service.create_tokens(user)
    return tokens
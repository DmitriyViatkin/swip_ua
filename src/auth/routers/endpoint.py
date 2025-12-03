from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from dishka.integrations.fastapi import FromDishka, inject

from src.auth.services.auth_service import AuthService
from config.infra.providers.auth_provider import AuthProvider

router = APIRouter()

@router.post("/token")
@inject
async def login(
    service: FromDishka[AuthService],
    form_data: OAuth2PasswordRequestForm = Depends(),

):
    user = await service.authenticate(form_data.username, form_data.password)
    tokens = service.create_tokens(user)
    return tokens
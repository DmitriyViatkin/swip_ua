from fastapi import APIRouter

from .routers.endpoint import router as autorization
from src.users.routers.create_user import router as create_user_router


router = APIRouter(prefix="/authorization", tags=["Authorization"])

# Подключаем все подроутеры


router.include_router(autorization)
router.include_router(create_user_router)
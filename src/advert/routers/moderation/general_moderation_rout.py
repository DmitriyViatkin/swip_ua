from fastapi import APIRouter, Depends

from ..moderation.moderation import router as moderation
from ..moderation.unmoderation import router as unmoderation
from ..moderation.all_advert_moderation import router as all_advert_moderation
from src.auth.dependencies import get_current_user
from src.users.models.users import User
from typing import Annotated
CurrentUser = Annotated[User, Depends(get_current_user)]

router=APIRouter(prefix="", tags=["Moderation"])

# Подключаем все подроутеры
router.include_router(all_advert_moderation)
router.include_router(moderation)
router.include_router(unmoderation)
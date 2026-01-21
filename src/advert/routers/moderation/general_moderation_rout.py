from fastapi import APIRouter

from ..moderation.moderation import router as moderation
from ..moderation.unmoderation import router as unmoderation
from ..moderation.all_advert_moderation import router as all_advert_moderation


router=APIRouter(prefix="", tags=["Moderation"])

# Подключаем все подроутеры
router.include_router(all_advert_moderation)
router.include_router(moderation)
router.include_router(unmoderation)
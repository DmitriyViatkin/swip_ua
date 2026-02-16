from fastapi import APIRouter

from src.users.routers.favorites_router.add_to_favorites import router as add_favorites
from src.users.routers.favorites_router.get_my_favorites import router as get_list_favorites
from src.users.routers.favorites_router.remove_from_favorites import router as remove_favorites



router=APIRouter(prefix="/favorites", tags=["Favorites"])

# Подключаем все подроутеры

router.include_router(add_favorites)
router.include_router(get_list_favorites)
router.include_router(remove_favorites)






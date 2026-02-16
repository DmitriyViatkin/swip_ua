from fastapi import APIRouter
from src.users.routers.black_list.add_black_list import router as add_blacklist
from src.users.routers.black_list.delete_from_black_list import router as remove_list
from src.users.routers.black_list.all_user_from_black_list import router as all_user_blacklist
from src.users.routers.black_list.all_user  import router as all_user


router = APIRouter(prefix="/black_list", tags=["Black List"] )

# Подключаем все подроутеры
router.include_router(all_user)
router.include_router(all_user_blacklist)
router.include_router(add_blacklist)
router.include_router(remove_list)


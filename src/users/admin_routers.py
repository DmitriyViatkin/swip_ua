from fastapi import APIRouter

from .routers.notarius_routers.all_routers_notary import router as notary
from .routers.black_list.all_router_black_list import router as blacklist

router = APIRouter(prefix="/admin", tags=["Admin"])

# Подключаем все подроутеры

router.include_router(notary)
router.include_router(blacklist)


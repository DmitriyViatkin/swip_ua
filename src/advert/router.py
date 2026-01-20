from fastapi import APIRouter

from .routers.create_adverts_routers import router as create_advert
from .routers.update_advers_routers import router as update_advert
from .routers.delete_adverts_routers import router as delete_advert
from .routers.all_adverts_routers import router as all_advert
from .routers.get_advert_by_id import router as advert_by_id
from .routers.promotion_routers.promotion_create_rout import router as promotion_create
from .routers.promotion_routers.promotion_update_rout import router as promotion_update


router=APIRouter(prefix="/adverts", tags=["Adverts"])

# Подключаем все подроутеры

router.include_router(all_advert)
router.include_router(create_advert)
router.include_router(advert_by_id)
router.include_router(update_advert)
router.include_router(delete_advert)
router.include_router(promotion_create)
router.include_router(promotion_update)




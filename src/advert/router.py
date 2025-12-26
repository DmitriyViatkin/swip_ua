from fastapi import APIRouter

from .routers.create_adverts_routers import router as create_advert
from .routers.update_advers_routers import router as update_advert
from .routers.delete_adverts_routers import router as delete_advert
from .routers.all_adverts_routers import router as all_advert
from .routers.gallery.add_forto_advert import router as add_gallery

router=APIRouter(prefix="/adverts", tags=["advert"])

# Подключаем все подроутеры

router.include_router(all_advert)
router.include_router(create_advert)
router.include_router(update_advert)
router.include_router(delete_advert)
router.include_router(add_gallery)

from fastapi import APIRouter

from .routers.create_adverts_routers import router as create_advert
from .routers.update_advers_routers import router as update_advert
from .routers.delete_adverts_routers import router as delete_advert
from .routers.all_adverts_routers import router as all_advert
from .routers.get_advert_by_id import router as advert_by_id
from .routers.gallery.add_forto_advert import router as add_gallery
from .routers.gallery.get_all_foto import router as get_foto
from .routers.gallery.replace_gallery_image  import router as replace_foto
from .routers.gallery.gallery_image_reorder import router as reorder_foto
from .routers.gallery.delete_image_gallery import router as delete_foto
from .routers.gallery.get_all_foto import router as get_foto


router=APIRouter(prefix="/adverts", tags=["advert"])

# Подключаем все подроутеры

router.include_router(all_advert)
router.include_router(create_advert)
router.include_router(advert_by_id)
router.include_router(update_advert)
router.include_router(delete_advert)


#Gallery
#router.include_router(add_gallery)
#router.include_router(get_foto)
#router.include_router(replace_foto)
#router.include_router(reorder_foto)
#router.include_router(delete_foto)

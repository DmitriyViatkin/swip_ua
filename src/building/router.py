from fastapi import APIRouter

from .routers.all_developer import router as all_dev
from .routers.personal_cabinet import router as cabinet
from .routers.update_infr import router as infrastructure
from .routers.create_house import router as house
from .routers.get_house import router as get_house
from .routers.update_house import router as house_update
from .routers.house_delete import  router as house_delete
from .routers.create_news import  router as create_news
from .routers.update_news import  router as update_news
from .routers.all_news import  router as all_news
from .routers.delete_news import  router as delete_news
from .routers.document import  router as document
from .routers.exel import  router as exel
from .routers.gallery import  router as gallery
from .routers.chessboard_rout.get_chessboard import router as chessboard
from .routers.chessboard_rout.all_chessboard import router as all_chessboard
from .routers.chessboard_rout.add_flat import router as add_flat

router = APIRouter(prefix="/development", tags=["Develop"])

# Подключаем все подроутеры

router.include_router(all_dev)
router.include_router(cabinet)
router.include_router(house)
router.include_router(get_house)
router.include_router(house_update)
router.include_router(house_delete)
router.include_router(infrastructure)
router.include_router(create_news)
router.include_router(update_news)
router.include_router(all_news)
router.include_router(delete_news)
router.include_router(document)
router.include_router(exel)
# router.include_router(gallery)
router.include_router(chessboard)
router.include_router(all_chessboard)
router.include_router(add_flat)
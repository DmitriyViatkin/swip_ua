from fastapi import APIRouter

from ..filters_routers.saved_filter_router import router as save_filter
from ..filters_routers.update_filter import router as update_filter
from ..filters_routers.get_result_filters import router as get_result_filters
from ..filters_routers.delete_filter import router as delete_filter
from ..filters_routers.search_adverts import router as search_adverts



router=APIRouter(prefix="/filters", tags=["Filters"])

# Подключаем все подроутеры

router.include_router(save_filter)
router.include_router(update_filter)
router.include_router(get_result_filters)
router.include_router(search_adverts)
router.include_router(delete_filter)





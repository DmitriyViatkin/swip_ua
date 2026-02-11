from fastapi import APIRouter

from ..complaint_router.create_complaint_router import router as create
from ..complaint_router.get_complaints_by_advert  import router as get_by_adverts
from ..complaint_router.get_all_complaints_for_moderation import router as get_for_moderation
from ..complaint_router.delete_complaint import router as delete



router=APIRouter(prefix="/complaint", tags=["Complaint"])

# Подключаем все подроутеры

router.include_router(create)
router.include_router(get_by_adverts)
router.include_router(get_for_moderation)

router.include_router(delete )





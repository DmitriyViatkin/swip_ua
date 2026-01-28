from fastapi import APIRouter

from src.users.routers.message.send_message import router as send_message
from src.users.routers.message.history_message import router as history_message




router=APIRouter(prefix="/message", tags=["Message"])

# Подключаем все подроутеры

router.include_router(send_message)
router.include_router(history_message)






from fastapi import APIRouter

from src.users.routers.get_user import router as get_user_router
from src.users.routers.notarius_routers.create_notary import router as create_notary
from src.users.routers.notarius_routers.update_notary import router as update_notary
from src.users.routers.notarius_routers.get_all import router as get_all_router
#Redirection

from src.users.routers.redirection.update_redirection import router as up_redirection_router
from src.users.routers.subscription.update_subscription import router as up_subscription_router

from src.users.routers.create_user import router as create_user_router
from src.users.routers.update_user import router as update_user_router
from src.users.routers.delete_user import router as delete_user_router
from src.users.routers.role_filter import router as role_filter_router

router = APIRouter(prefix="/notary",  )

# Подключаем все подроутеры
router.include_router(create_notary)
router.include_router(update_notary)
router.include_router(get_all_router)

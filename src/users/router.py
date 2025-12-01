from fastapi import APIRouter

from .routers.get_user import router as get_user_router
from .routers.create_notification import router as create_notification_router
from .routers.update_notification import router as update_notification_router
from .routers.get_all import router as get_all_router
#Redirection
from .routers.redirection.update_redirection import router as up_redirection_router
from .routers.subscription.update_subscription import router as up_subscription_router

from .routers.create_user import router as create_user_router
from .routers.update_user import router as update_user_router
from .routers.delete_user import router as delete_user_router
from .routers.role_filter import router as role_filter_router

router = APIRouter(prefix="/users", tags=["Users"])

# Подключаем все подроутеры

router.include_router(get_all_router)
router.include_router(get_user_router)

router.include_router(create_user_router)
#router.include_router(create_notification_router)

router.include_router(update_user_router)
router.include_router(update_notification_router)
router.include_router(up_redirection_router)
router.include_router(up_subscription_router)

router.include_router(delete_user_router)
router.include_router(role_filter_router)
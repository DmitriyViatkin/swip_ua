from fastapi import APIRouter

from .routers.endpoint import router as authorization
from src.users.routers.create_user import router as create_user_router
from src.auth.routers.request_email import router as request_email
from src.auth.routers.verify_request import router as verify_email
from src.auth.routers.password_confirm import router as confirm_password_router
from src.auth.routers.password_request import router as password_request_router



router = APIRouter(  tags=["Authorization"])



router.include_router(request_email)

router.include_router(verify_email)

router.include_router(authorization)

router.include_router(create_user_router)

router.include_router(password_request_router)

router.include_router(confirm_password_router)



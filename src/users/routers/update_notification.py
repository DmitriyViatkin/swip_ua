from fastapi import APIRouter, Depends
from dishka.integrations.fastapi import FromDishka, inject
from typing import Annotated
from src.auth.role_dependencies import require_roles
from src.auth.dependencies import get_current_user
from  src.enums import UserRole
from src.users.models.users import User
from src.users.schemas.notification.update import NotificationUpdate
CurrentUser = Annotated[User, Depends(require_roles(UserRole.CLIENT, UserRole.ADMIN))]
from src.users.services.notification_service import NotificationService

router = APIRouter()

@router.put("/user/update_notification/{user_id}")
@inject
async def update_notification(
    user_id: int,
    data: NotificationUpdate,
    service: FromDishka[NotificationService],
        user: CurrentUser
):
    return await service.update_notification(user_id, data)
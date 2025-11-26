from fastapi import APIRouter
from dishka.integrations.fastapi import FromDishka, inject

from src.users.schemas.notification.update import NotificationUpdate

from src.users.services.notification_service import NotificationService

router = APIRouter()

@router.put("/user/update_notification/{user_id}")
@inject
async def update_notification(
    user_id: int,
    data: NotificationUpdate,
    service: FromDishka[NotificationService]
):
    return await service.update_notification(user_id, data)
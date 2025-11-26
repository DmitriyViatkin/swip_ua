from fastapi import APIRouter
from dishka.integrations.fastapi import FromDishka, inject

from src.users.schemas.notification.create import NotificationCreate

from src.users.services.notification_service import NotificationService

router = APIRouter()

@router.post("/user/create_notification/")
@inject
async def create_notification(data: NotificationCreate, service: FromDishka[NotificationService]):
    return await service.create_notification(data)

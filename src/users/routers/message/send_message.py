from fastapi import APIRouter, Depends, status
from dishka.integrations.fastapi import FromDishka, inject
from typing import List

from src.auth.dependencies import get_current_user
from src.users.models.users import User
from src.users.services.message_serv import MessageService
from src.users.schemas.message.message_create_sch import MessageCreate
from src.users.schemas.message.message_read_sch import MessageRead

router = APIRouter( )

@router.post("/send", response_model=MessageRead, status_code=status.HTTP_201_CREATED)
@inject
async def send_message(
    data: MessageCreate,
    service: FromDishka[MessageService],
    current_user: User = Depends(get_current_user),
):
    """
    Отправить сообщение. Dishka сама создаст сервис и репозиторий.
    """
    return await service.send_message(sender=current_user, data=data)
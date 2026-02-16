from fastapi import APIRouter, Depends, status
from dishka.integrations.fastapi import FromDishka, inject
from typing import List

from src.auth.dependencies import get_current_user
from src.users.models.users import User
from src.users.services.message_serv import MessageService
from src.users.schemas.message.message_create_sch import MessageCreate
from src.users.schemas.message.message_read_sch import MessageRead
from src.users.models.users import User
from  src.enums import UserRole
from typing import Annotated
from src.auth.role_dependencies import require_roles
from src.auth.dependencies import get_current_user
CurrentUser = Annotated[User, Depends(require_roles(UserRole.CLIENT, UserRole.ADMIN))]

router = APIRouter( )

@router.post("/send", response_model=MessageRead, status_code=status.HTTP_201_CREATED)
@inject
async def send_message(
    data: MessageCreate,
    service: FromDishka[MessageService],
    user: CurrentUser,
):
    """
    Отправить сообщение. Dishka сама создаст сервис и репозиторий.
    """
    return await service.send_message(sender= user, data=data)
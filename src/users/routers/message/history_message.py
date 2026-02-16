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



@router.get("/history/{contact_id}", response_model=List[MessageRead])
@inject
async def get_history(
    contact_id: int,
    service: FromDishka[MessageService],
    user: CurrentUser,
):
    """
    История переписки с пользователем.
    """
    return await service.get_messages_with_user(user_id=current_user.id, contact_id=contact_id)
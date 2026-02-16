from fastapi import APIRouter, Depends
from dishka.integrations.fastapi import FromDishka
from src.users.schemas.redirections.create import RedirectionCreate
from src.users.schemas.redirections.update import   RedirectionUpdate
from src.users.schemas.redirections.read import   RedirectionRead
from src.users.services.redirection_service import RedirectionService
from src.users.models.users import User
from  src.enums import UserRole
from typing import Annotated
from src.auth.role_dependencies import require_roles
from src.auth.dependencies import get_current_user
CurrentUser = Annotated[User, Depends(require_roles(UserRole.CLIENT, UserRole.ADMIN))]

router = APIRouter()



@router.delete("/user/delete_redirection/{id}")
async def delete_redirection (id: int, user: CurrentUser,
                              service: FromDishka[RedirectionService]):
    await service.delete_redirection(id)
    return {"status": "ok"}
from fastapi import APIRouter, Depends
from dishka.integrations.fastapi import FromDishka,inject
from src.users.schemas.redirections.create import RedirectionCreate
from src.users.schemas.redirections.update import   RedirectionUpdate
from src.users.schemas.redirections.read import   RedirectionRead
from src.users.services.redirection_service import RedirectionService
from typing import Annotated
from src.auth.role_dependencies import require_roles
from src.auth.dependencies import get_current_user
from  src.enums import UserRole
from src.users.models.users import User
CurrentUser = Annotated[User, Depends(require_roles(UserRole.CLIENT, UserRole.ADMIN))]


router = APIRouter()


@router.put("/user/redirection/{id}", response_model=RedirectionRead)
@inject

async def update_redirection (id: int,

                              data: RedirectionUpdate,
                              service: FromDishka[RedirectionService],
                              user: CurrentUser):
    return await service.update_redirection(id, data)


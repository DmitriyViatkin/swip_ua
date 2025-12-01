from fastapi import APIRouter
from dishka.integrations.fastapi import FromDishka,inject
from src.users.schemas.redirections.create import RedirectionCreate
from src.users.schemas.redirections.update import   RedirectionUpdate
from src.users.schemas.redirections.read import   RedirectionRead
from src.users.services.redirection_service import RedirectionService

router = APIRouter()


@router.put("/user/redirection/{id}", response_model=RedirectionRead)
@inject
async def update_redirection (id: int, data: RedirectionUpdate, service: FromDishka[RedirectionService]):
    return await service.update_redirection(id, data)


from fastapi import APIRouter
from dishka.integrations.fastapi import FromDishka
from src.users.schemas.redirections.create import RedirectionCreate
from src.users.schemas.redirections.update import   RedirectionUpdate
from src.users.schemas.redirections.read import   RedirectionRead
from src.users.services.redirection_service import RedirectionService

router = APIRouter()



@router.delete("/user/delete_redirection/{id}")
async def delete_redirection (id: int, service: FromDishka[RedirectionService]):
    await service.delete_redirection(id)
    return {"status": "ok"}
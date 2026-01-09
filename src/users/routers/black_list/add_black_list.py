
from fastapi import APIRouter
from dishka.integrations.fastapi import FromDishka, inject

from src.users.schemas.black_list.create import BlackListCreate

from src.users.services.black_list_serv import BlackListService

router = APIRouter()

@router.post("/blacklist/add/")
@inject
async def add_from_black_list (data: BlackListCreate, service: FromDishka[BlackListService]):
    return await service.add_to_blacklist(data.user_id)
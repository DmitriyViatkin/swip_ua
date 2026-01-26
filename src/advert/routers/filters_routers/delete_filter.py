from src.advert.schemas.filters.filters_update_sch import FilterUpdate
from src.advert.schemas.filters.filters_read_sch import FilterRead
from dishka.integrations.fastapi import FromDishka, inject
from src.advert.services.filter_serv import FilterService
from fastapi import  HTTPException,APIRouter, status
from src.users.models import User
from typing import Annotated
from fastapi import Depends
from src.auth.dependencies import get_current_user
# Ось це визначення аліаса:
CurrentUser = Annotated[User, Depends(get_current_user)]
router = APIRouter( )


@router.delete("/{filter_id}/delete", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_filter(
        filter_id: int,
        service: FromDishka[FilterService],
        user: CurrentUser,
):

    print(f"--- ROUTER DEBUG ---")
    print(f"Target filter_id: {filter_id}")
    print(f"Current user object: {user}")
    print(f"Current user.id from token: {user.id}")
    print(f"--------------------")

    """Видалення фільтра."""

    success = await service.delete_filter(filter_id=filter_id, user_id=user.id)

    if not success:
        raise HTTPException(status_code=404, detail="Фільтр не знайдено")
    return None



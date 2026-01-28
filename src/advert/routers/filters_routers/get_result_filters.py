from fastapi import APIRouter, status, HTTPException, Depends
from dishka.integrations.fastapi import FromDishka, inject
from src.auth.dependencies import get_current_user
from src.users.models.users import User
from src.advert.services.filter_serv import FilterService

router = APIRouter(   )


@router.get("/{filter_id}/results")
@inject
async def get_existing_filter_results(
        filter_id: int,
        current_user: User = Depends(get_current_user),
        service: FromDishka[FilterService] = None,
):
    ads = await service.get_results_by_existing_filter(
        filter_id=filter_id,
        user_id=current_user.id
    )

    if ads is None:
        raise HTTPException(
            status_code=404,
            detail="Фільтр не знайдено або він належить іншому користувачу"
        )

    return ads
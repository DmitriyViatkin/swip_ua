from fastapi import APIRouter, status, HTTPException, Depends
from dishka.integrations.fastapi import FromDishka, inject
from src.auth.dependencies import get_current_user  # Імпортуй свою залежність
from src.users.models.users import User
from src.advert.services.filter_serv import FilterService

router = APIRouter(prefix="/filters", tags=["Filters"])


@router.get("/{filter_id}/results")
@inject
async def get_existing_filter_results(
        filter_id: int,
        service: FromDishka[FilterService]
):
    """Пошук за збереженим ID (тимчасово без авторизації)."""

    # Оскільки ми прибрали CurrentUser, підставимо твій ID (24) вручну
    test_user_id = 24

    ads = await service.get_results_by_existing_filter(
        filter_id=filter_id,
        user_id=test_user_id
    )

    if ads is None:
        raise HTTPException(
            status_code=404,
            detail="Фільтр не знайдено або він належить іншому юзеру"
        )

    return ads
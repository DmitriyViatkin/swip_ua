from fastapi import APIRouter, HTTPException
from dishka.integrations.fastapi import FromDishka,inject
from src.users.schemas.redirections.create import RedirectionCreate
from src.users.schemas.subscription.update import   SubscriptionUpdate
from src.users.schemas.subscription.read import   SubscriptionRead
from src.users.services.subscription_service import SubscriptionService

router = APIRouter()


@router.put("/user/subscription/{user_id}", response_model=SubscriptionRead)
@inject
async def update_subscription(
    user_id: int,
    data: SubscriptionUpdate,
    service: FromDishka[SubscriptionService],
):
    # Викликаємо оновлення саме за ID користувача
    result = await service.update_by_user_id(user_id, data)
    if result is None:
        raise HTTPException(status_code=404, detail="Subscription for this user not found")
    return result


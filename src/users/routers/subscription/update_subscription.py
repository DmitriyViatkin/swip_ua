from fastapi import APIRouter
from dishka.integrations.fastapi import FromDishka,inject
from src.users.schemas.redirections.create import RedirectionCreate
from src.users.schemas.subscription.update import   SubscriptionUpdate
from src.users.schemas.subscription.read import   SubscriptionRead
from src.users.services.subscription_service import SubscriptionService

router = APIRouter()


@router.put("/user/subscription/{id}", response_model=SubscriptionRead)
@inject


async def update_subscription(
    subscription_id: int,
    data: SubscriptionUpdate,
    service: FromDishka[SubscriptionService],
):
    return await service.update(subscription_id, data)


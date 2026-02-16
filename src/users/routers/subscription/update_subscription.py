from fastapi import APIRouter, HTTPException, Depends
from dishka.integrations.fastapi import FromDishka,inject
from src.users.schemas.redirections.create import RedirectionCreate
from src.users.schemas.subscription.update import   SubscriptionUpdate
from src.users.schemas.subscription.read import   SubscriptionRead
from src.users.services.subscription_service import SubscriptionService
from typing import Annotated
from src.auth.role_dependencies import require_roles
from src.auth.dependencies import get_current_user
from  src.enums import UserRole
from src.users.models.users import User
CurrentUser = Annotated[User, Depends(require_roles(UserRole.CLIENT, UserRole.ADMIN))]


router = APIRouter()


@router.put("/user/subscription/{user_id}", response_model=SubscriptionRead)
@inject
async def update_subscription(
    user_id: int,
    data: SubscriptionUpdate,
    service: FromDishka[SubscriptionService],
    user: CurrentUser
):

    result = await service.update_by_user_id(user_id, data)
    if result is None:
        raise HTTPException(status_code=404, detail="Subscription for this user not found")
    return result


from typing import Optional, List
from src.users.repositories.subscriptions_repository import SubscriptionRepository
from src.users.schemas.subscription.read import SubscriptionRead
from src.users.schemas.subscription.create import SubscriptionCreate
from src.users.schemas.subscription.update import SubscriptionUpdate


class SubscriptionService:
    """Business logic for Subscription."""

    def __init__(self, repo: SubscriptionRepository):
        self.repo = repo

    async def get_subscription(self, subscription_id: int) -> Optional[SubscriptionRead]:
        obj = await self.repo.get_by_id(subscription_id)
        if not obj:
            return None
        return SubscriptionRead.model_validate(obj)

    async def get_user_subscription(self, user_id: int) -> Optional[SubscriptionRead]:
        obj = await self.repo.get_by_user_id(user_id)
        if not obj:
            return None
        return SubscriptionRead.model_validate(obj)

    async def get_all(self) -> List[SubscriptionRead]:
        items = await self.repo.get_all()
        return [SubscriptionRead.model_validate(i) for i in items]

    async def create(self, data: SubscriptionCreate) -> SubscriptionRead:
        obj = await self.repo.create(**data.model_dump())
        return SubscriptionRead.model_validate(obj)

    async def update_by_user_id(self, user_id: int, data: SubscriptionUpdate) -> Optional[SubscriptionRead]:
        # Створюємо словник для оновлення, виключаючи user_id, щоб не було дублювання
        update_data = data.model_dump(exclude_unset=True)
        update_data.pop("user_id", None)  # Видаляємо user_id, якщо він там є

        obj = await self.repo.update_by_user_id(user_id, **update_data)

        if not obj:
            return None
        return SubscriptionRead.model_validate(obj)

    async def delete(self, subscription_id: int) -> None:
        await self.repo.delete(subscription_id)

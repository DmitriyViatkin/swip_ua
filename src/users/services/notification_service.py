from typing import List, Optional
from src.users.repositories.notification_repository import NotificationRepository
from src.users.schemas.notification.create import NotificationCreate
from src.users.schemas.notification.update import NotificationUpdate
from src.users.schemas.notification.read import NotificationRead
from src.enums import UserRole


class NotificationService:
    """ Business logic for Notification. """

    def __init__ (self, repo: NotificationRepository) :
        self.repo = repo

    async def get_notification (self, notification_id: int ) -> Optional[NotificationRead]:

        notification =  await self.repo.get_by_id(notification_id)

        if not notification:
            return None
        return  NotificationRead.model_validate(notification)

    async def create_notification(self, data: NotificationCreate) -> NotificationRead:
        notification = await self.repo.create(**data.model_dump())  # Було model_damp
        return NotificationRead.model_validate(notification)

    async def update_notification(self, user_id: int, data: NotificationUpdate) -> Optional[NotificationRead]:
        # 1. Спробуємо оновити
        notification = await self.repo.update(user_id, **data.model_dump(exclude_unset=True))

        # 2. Якщо не знайшли (повернуло None), то створюємо новий запис
        if not notification:
            # Додаємо client_id до даних для створення
            create_data = data.model_dump(exclude_unset=True)
            create_data["client_id"] = user_id
            notification = await self.repo.create(**create_data)

        return NotificationRead.model_validate(notification)

    async def delete_notification(self, notification_id: int) -> None:
        await self.repo.delete(notification_id)



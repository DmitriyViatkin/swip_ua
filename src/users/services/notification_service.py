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
        return  NotificationrRead.model_validate(notification)
    async def create_notification (self, data:NotificationCreate) -> NotificationRead:
        notification = await self.repo.create(**data.model_damp())
        return NotificationrRead.model_validate(notification)

    async def update_notification (self, notification_id: int, data: NotificationUpdate) -> Optional[
        NotificationRead]:

        notification = await self.repo.update(notification_id, **data.model_dump(exclude_unset=True))
        if not notification:
            return None
        return NotificationRead.model_validate(user)

    async def delete_notification(self, notification_id: int) -> None:
        await self.repo.delete(notification_id)



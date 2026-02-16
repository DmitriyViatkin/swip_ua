from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.engine import Result
# Note: Assuming your Notification model is correctly imported
# from src.notifications.models import Notification
from src.users.models import Notification # Using your import path for now
from src.users.schemas.notification.create import NotificationCreate # Assuming this Pydantic schema exists

class NotificationRepository:
    """ Repository for Notification model, using async SQLAlchemy 2.0 style. """

    def __init__(self, session: AsyncSession):
        self.session = session

    # --- CRUD Operations ---

    async def get_by_id(self, notification_id: int) -> Optional[Notification]:
        """ Fetches a single notification by its ID. """
        stmt = select(Notification).where(Notification.id == notification_id)
        result: Result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, **data) -> Notification:
        """ Creates a new notification record. """
        # **Note:** It's better to accept a Pydantic schema here for type safety.
        notification = Notification(**data)
        self.session.add(notification)
        await self.session.commit()
        await self.session.refresh(notification)
        return notification

    async def update (self, user_id: int, **data) -> Optional[Notification]:
        stmt = (
            update(Notification)
            .where(Notification.client_id == user_id)  # Шукаємо за власником, а не за ID запису
            .values(**data)
            .returning(Notification)
        )
        result: Result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one_or_none()

    async def delete(self, notification_id: int) -> None:
        """ Deletes a notification by its ID. """
        stmt = delete(Notification).where(Notification.id == notification_id)
        await self.session.execute(stmt)
        await self.session.commit()

    # --- Notification-Specific Logic ---

    async def get_notifications_for_client(
        self,
        client_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Notification]:
        """ Fetches notifications for a specific client, with pagination. """
        stmt = (
            select(Notification)
            .where(Notification.client_id == client_id)
            .offset(skip)
            .limit(limit)
        )
        result: Result = await self.session.execute(stmt)

        return list(result.scalars().all())

    async def get_unread_notifications_for_client(
        self,
        client_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Notification]:
        """ Fetches UNREAD notifications for a specific client. """
        stmt = (
            select(Notification)
            .where(Notification.client_id == client_id)
            .where(Notification.turn_off == False) # Assuming turn_off == False means unread
            .offset(skip)
            .limit(limit)
        )
        result: Result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def mark_as_read(self, notification_id: int) -> Optional[Notification]:
        """ Updates the 'turn_off' status (marks as read) for a notification. """

        updated_notification = await self.update(
            notification_id,
            turn_off=True
        )
        return updated_notification

    async def mark_all_as_read_for_client(self, client_id: int) -> None:
        """ Marks all unread notifications for a client as read. """
        stmt = (
            update(Notification)
            .where(Notification.client_id == client_id)
            .where(Notification.turn_off == False)
            .values(turn_off=True)
        )
        await self.session.execute(stmt)
        await self.session.commit()
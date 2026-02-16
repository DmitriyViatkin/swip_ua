from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.repositories.notification_repository import NotificationRepository
from src.users.services.notification_service import NotificationService

class NotificationProvider(Provider):
    """ DI provider for notification module. """
    scope = Scope.REQUEST

    @provide
    def notification_repository(self, session: AsyncSession) -> NotificationRepository:
        return NotificationRepository(session)

    @provide
    def notification_service(self, notification_repository: NotificationRepository) -> NotificationService:
        return NotificationService(notification_repository)
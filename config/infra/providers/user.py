from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.repositories.black_list_repo import BlackListRepo
from src.users.repositories.user_repository import UserRepository
from src.users.services.black_list_serv import BlackListService
from src.users.services.user_service import UserService
from src.users.repositories.subscriptions_repository import SubscriptionRepository
from src.users.repositories.notification_repository import NotificationRepository
from src.users.repositories.redirection_repository import RedirectionRepository


class UserProvider(Provider):

    @provide(scope=Scope.REQUEST)
    async def user_repository(self, session: AsyncSession) -> UserRepository:
        return UserRepository(session)

    @provide(scope=Scope.REQUEST)
    async def subscription_repository(self, session: AsyncSession) -> SubscriptionRepository:
        return SubscriptionRepository(session)

    @provide(scope=Scope.REQUEST)
    async def notification_repository(self, session: AsyncSession) -> NotificationRepository:
        return NotificationRepository(session)

    @provide(scope=Scope.REQUEST)
    async def redirection_repository(self, session: AsyncSession) -> RedirectionRepository:
        return RedirectionRepository(session)

    @provide(scope=Scope.REQUEST)
    async def user_service(
        self,
        user_repository: UserRepository,
        subscription_repository: SubscriptionRepository,
        notification_repository: NotificationRepository,
        redirection_repository: RedirectionRepository,
    ) -> UserService:
        return UserService(
            user_repository,
            subscription_repository,
            notification_repository,
            redirection_repository,
        )

    black_list_repo = provide(
        BlackListRepo, scope=Scope.REQUEST
    )
    black_list_serv = provide(
        BlackListService, scope=Scope.REQUEST
    )
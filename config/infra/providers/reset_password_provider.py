from dishka import Provider, Scope, provide
from src.users.repositories.user_repository import UserRepository
from config.infra.providers.user import UserProvider
from src.auth.services.reset_password_service import PasswordResetService



class PasswordResetServiceProvider(Provider):

    @provide(scope=Scope.REQUEST)
    async def password_reset_service(
        self,
        user_repo: UserRepository,
    ) -> PasswordResetService:
        return PasswordResetService(user_repo)
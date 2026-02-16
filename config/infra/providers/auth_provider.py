from dishka import Provider, provide,Scope



from src.auth.services.jwt_service import JWTService
from src.users.repositories.user_repository import UserRepository
from src.auth.services.auth_service import AuthService

class AuthProvider(Provider):
    scope = Scope.REQUEST

    jwt_service = provide(JWTService)
    user_repo = provide(UserRepository)

    @provide
    def auth_service(self, user_repo: UserRepository, jwt_service: JWTService) -> AuthService:
        return AuthService(user_repo, jwt_service)
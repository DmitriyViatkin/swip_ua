from dishka import Provider, Scope, provide
# repositories
from src.advert.repositories.advert_repo import AdvertRepository

# services
from src.advert.services.advert_serv import AdvertService


class AdvertProvider(Provider):
    """Main DI provider for the Adverts module."""

    # -------------------- REPOSITORIES --------------------

    adverts_repo = provide(
        AdvertRepository, scope=Scope.REQUEST
    )

    # -------------------- SERVICES --------------------

    adverts_service = provide(
        AdvertService,
        scope=Scope.REQUEST
    )

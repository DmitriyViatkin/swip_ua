from dishka import Provider, Scope, provide
# repositories
from src.advert.repositories.filters_repo import FilterRepository

# services
from src.advert.services.filter_serv import FilterService


class FilterProvider(Provider):
    """Main DI provider for the Filters module."""

    # -------------------- SERVICES --------------------

    filter_serv = provide(
        FilterService, scope=Scope.REQUEST
    )
    # -------------------- REPOSITORIES --------------------
    filter_repo = provide(
        FilterRepository, scope=Scope.REQUEST
    )
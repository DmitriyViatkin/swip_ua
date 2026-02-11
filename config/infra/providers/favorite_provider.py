from dishka import  Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.repositories.favoriete_repo import FavoritesRepository
from src.users.services.favorite_serv import FavoritesService

class FavoriteProviders(Provider):
    """ DI provider for promotion module. """

    # -------------------- REPOSITORIES --------------------

    # -------------------- SERVICES --------------------
    favorite_repo= provide(
       FavoritesRepository, scope= Scope.REQUEST
    )
    favorite_serv = provide(
        FavoritesService, scope=Scope.REQUEST
    )
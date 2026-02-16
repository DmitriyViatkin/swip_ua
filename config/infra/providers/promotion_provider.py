from dishka import  Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.advert.repositories.promotion_repo import PromotionRepository
from src.advert.services.promotion_serv import PromotionService

class PromotionProviders(Provider):
    """ DI provider for promotion module. """

    # -------------------- REPOSITORIES --------------------
    promotion_repo = provide(
        PromotionRepository, scope=Scope.REQUEST
    )
    # -------------------- SERVICES --------------------
    promotion_serv= provide(
        PromotionService, scope= Scope.REQUEST
    )
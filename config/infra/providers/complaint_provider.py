from dishka import  Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.advert.repositories.complaint_repo import ComplaintsRepository
from src.advert.services.complaint_serv import ComplaintsService

class ComplaintsProviders(Provider):
    """ DI provider for promotion module. """

    # -------------------- REPOSITORIES --------------------


    complaint_repo= provide(
       ComplaintsRepository, scope= Scope.REQUEST
    )
    # -------------------- SERVICES --------------------
    complaint_serv = provide(
        ComplaintsService, scope=Scope.REQUEST
    )
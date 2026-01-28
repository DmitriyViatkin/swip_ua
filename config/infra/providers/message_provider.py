from dishka import  Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.repositories.message_repo import MessageRepository
from src.users.services.message_serv import MessageService

class MessageProviders(Provider):
    """ DI provider for promotion module. """

    # -------------------- REPOSITORIES --------------------

    # -------------------- SERVICES --------------------
    message_repo= provide(
       MessageRepository, scope= Scope.REQUEST
    )
    message_serv = provide(
        MessageService, scope=Scope.REQUEST
    )
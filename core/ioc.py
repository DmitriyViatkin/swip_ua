""" Main dependens """
from core.infra.config.settings import infra_settings
from core.infra.providers.postgres import PostgresProvider
from core.infra.providers.redis import RedisProvider
#from src.core.infra.providers.repositories import RepositoriesProvider
from core.infra.config.settings import InfraSettings
from dishka import make_async_container
from core.infra.providers.user  import UserProvider

# список провайдеров

container = make_async_container(

    PostgresProvider(),
    RedisProvider(),
    UserProvider(),
    context={
        InfraSettings: infra_settings,
    }
)

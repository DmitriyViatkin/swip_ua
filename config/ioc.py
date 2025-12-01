""" Main dependens """
from config.infra.config.settings import infra_settings
from config.infra.providers.postgres import PostgresProvider
from config.infra.providers.redis import RedisProvider
#from src.core.infra.providers.repositories import RepositoriesProvider
from config.infra.config.settings import InfraSettings
from dishka import make_async_container
from config.infra.providers.user  import UserProvider
from config.infra.providers.redirection import RedirectionProvider
from config.infra.providers.notification  import NotificationProvider
from config.infra.providers.subscription  import SubscriptionProvider


container = make_async_container(

    PostgresProvider(),
    SubscriptionProvider(),
    RedirectionProvider(),
    RedisProvider(),
    UserProvider(),
    NotificationProvider(),
    context={
        InfraSettings: infra_settings,
    }
)

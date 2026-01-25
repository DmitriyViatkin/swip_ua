""" Main dependens """
from config.infra.config.settings import infra_settings

from config.infra.providers.redis import RedisProvider

from config.infra.config.settings import InfraSettings
from dishka import make_async_container
from config.infra.providers.postgres  import PostgresProvider
from config.infra.providers.user  import UserProvider
from config.infra.providers.redirection import RedirectionProvider
from config.infra.providers.notification  import NotificationProvider
from config.infra.providers.subscription  import SubscriptionProvider
from config.infra.providers.auth_provider  import AuthProvider
from config.infra.providers.reset_password_provider  import PasswordResetServiceProvider
from config.infra.providers.building_provider  import BuildingProvider
from config.infra.providers.advert_provider import AdvertProvider
from config.infra.providers.gallery_provider import GalleryProvider
from config.infra.providers.promotion_provider import PromotionProviders
from config.infra.providers.filter_provider import FilterProvider

container = make_async_container(

    PostgresProvider(),
    SubscriptionProvider(),
    RedirectionProvider(),
    RedisProvider(),
    UserProvider(),
    AuthProvider(),
    NotificationProvider(),
    BuildingProvider(),
    PasswordResetServiceProvider(),
    AdvertProvider(),
    GalleryProvider(),
    PromotionProviders(),
    FilterProvider(),
    context={
        InfraSettings: infra_settings,
    }
)

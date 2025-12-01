from dishka import Provider, Scope, provide
from src.users.repositories.subscriptions_repository import SubscriptionRepository
from src.users.services.subscription_service import SubscriptionService


class SubscriptionProvider(Provider):

    repository = provide(SubscriptionRepository, scope=Scope.REQUEST)
    service = provide(SubscriptionService, scope=Scope.REQUEST)
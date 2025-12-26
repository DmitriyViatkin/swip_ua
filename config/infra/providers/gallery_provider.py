from dishka import Provider, Scope, provide
# repositories
from src.advert.repositories.advert_repo import AdvertRepository

# services
from src.advert.services.gallery_image_service import GalleryImageService
class GalleryProvider(Provider):
    """Main DI provider for the Adverts module."""

    # -------------------- REPOSITORIES --------------------

    gallery_image_serv = provide(
        GalleryImageService, scope=Scope.REQUEST
    )
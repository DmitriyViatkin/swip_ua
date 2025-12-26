from dishka import Provider, Scope, provide

# repositories
from src.building.repositories.advantages_of_home import AdvantagesOfHomeRepository
from src.building.repositories.corps import CorpsRepository
from src.building.repositories.document import DocumentRepository
from src.building.repositories.flat import FlatRepository
from src.building.repositories.floor import FloorRepository
from src.building.repositories.house import HouseRepository
from src.building.repositories.infrastructure import InfrastructureRepository
from src.building.repositories.news import NewsRepository
from src.building.repositories.registration_and_payment import RegistrationAndPaymentRepository
from src.building.repositories.riser import RiserRepository
from src.building.repositories.section import SectionRepository

# services
from src.building.services.advantages_of_home import AdvantagesOfHomeService
from src.building.services.corps import CorpsService
from src.building.services.document import DocumentService
from src.building.services.flat import FlatService
from src.building.services.floor import FloorService
from src.building.services.house import HouseService
from src.building.services.infrastructure import InfrastructureService
from src.building.services.news import NewsService
from src.building.services.registration_and_payment import RegistrationAndPaymentService
from src.building.services.riser import RiserService
from src.building.services.section import SectionService
from src.building.services.personal_cabinet_service import PersonalCabinetService
from src.advert.services.gallery_serv import GalleryService

class BuildingProvider(Provider):
    """Main DI provider for the Building module."""

    # -------------------- REPOSITORIES --------------------

    advantages_repo = provide(
        AdvantagesOfHomeRepository,
        scope=Scope.REQUEST
    )

    corps_repo = provide(
        CorpsRepository,
        scope=Scope.REQUEST
    )

    document_repo = provide(
        DocumentRepository,
        scope=Scope.REQUEST
    )

    flat_repo = provide(
        FlatRepository,
        scope=Scope.REQUEST
    )

    floor_repo = provide(
        FloorRepository,
        scope=Scope.REQUEST
    )

    house_repo = provide(
        HouseRepository,
        scope=Scope.REQUEST
    )

    infrastructure_repo = provide(
        InfrastructureRepository,
        scope=Scope.REQUEST
    )

    news_repo = provide(
        NewsRepository,
        scope=Scope.REQUEST
    )

    registration_repo = provide(
        RegistrationAndPaymentRepository,
        scope=Scope.REQUEST
    )

    riser_repo = provide(
        RiserRepository,
        scope=Scope.REQUEST
    )

    section_repo = provide(
        SectionRepository,
        scope=Scope.REQUEST
    )

    # -------------------- SERVICES --------------------

    advantages_service = provide(
        AdvantagesOfHomeService,
        scope=Scope.REQUEST
    )

    corps_service = provide(
        CorpsService,
        scope=Scope.REQUEST
    )

    document_service = provide(
        DocumentService,
        scope=Scope.REQUEST
    )

    flat_service = provide(
        FlatService,
        scope=Scope.REQUEST
    )

    floor_service = provide(
        FloorService,
        scope=Scope.REQUEST
    )

    house_service = provide(
        HouseService,
        scope=Scope.REQUEST
    )

    infrastructure_service = provide(
        InfrastructureService,
        scope=Scope.REQUEST
    )

    news_service = provide(
        NewsService,
        scope=Scope.REQUEST
    )

    registration_service = provide(
        RegistrationAndPaymentService,
        scope=Scope.REQUEST
    )

    riser_service = provide(
        RiserService,
        scope=Scope.REQUEST
    )

    section_service = provide(
        SectionService,
        scope=Scope.REQUEST
    )

    personal_cabinet_service = provide(
        PersonalCabinetService,
        scope=Scope.REQUEST
    )


    gallery_service = provide(GalleryService, scope=Scope.REQUEST)

from src.users.repositories.user_repository import UserRepository
from src.users.schemas.user import UserRead

from ..repositories.house import HouseRepository
from ..repositories.news import NewsRepository
from ..repositories.document import DocumentRepository
from ..repositories.infrastructure import InfrastructureRepository
from ..repositories.registration_and_payment import RegistrationAndPaymentRepository
from src.building.schemas.personal_cabinet import PersonalCabinet
from src.building.schemas.house import HouseRead
from src.building.schemas.news import NewsRead
from src.building.schemas.document import DocumentRead
from src.building.schemas.infrastructure import InfrastructureRead
from src.building.schemas.registration_and_payment import RegistrationPaymentRead

class PersonalCabinetService:
    def __init__(
        self,
        user_repo: UserRepository,
        house_repo: HouseRepository,
        news_repo: NewsRepository,
        doc_repo: DocumentRepository,
        infra_repo: InfrastructureRepository,
        regpay_repo: RegistrationAndPaymentRepository,
    ):
        self.user_repo = user_repo
        self.house_repo = house_repo
        self.news_repo = news_repo
        self.doc_repo = doc_repo
        self.infra_repo = infra_repo
        self.regpay_repo = regpay_repo

    async def get_personal_cabinet(self, user_id: int) -> PersonalCabinet:
        user = await self.user_repo.get_by_id(user_id)

        house = await self.house_repo.get_by_user_id(user_id)
        if not house:
            return PersonalCabinet(
                user=UserRead.model_validate(user),
                house=None,
                news=[],
                document=[],
                infrastructure=None,
                registration_payment=None,
            )

        house_id = house.id

        news = await self.news_repo.get_last_by_house(house_id)
        documents = await self.doc_repo.get_by_house_id(house_id)
        infra = await self.infra_repo.get_by_house_id(house_id)
        regpay = await self.regpay_repo.get_by_house_id(house_id)

        return PersonalCabinet(
            user=UserRead.model_validate(user),
            house=HouseRead.model_validate(house),
            news=[NewsRead.model_validate(x) for x in news],
            document=[DocumentRead.model_validate(x) for x in documents],
            infrastructure=InfrastructureRead.model_validate(infra) if infra else None,
            registration_payment=RegistrationPaymentRead.model_validate(regpay) if regpay else None,
        )

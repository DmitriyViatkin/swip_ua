from ..schemas.advert.advert_create_sch import AdvertCreate
from ..schemas.advert.advert_update_sch import AdvertUpdate
from src.advert.repositories.advert_repo import AdvertRepository
from sqlalchemy.ext.asyncio import AsyncSession


class AdvertService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = AdvertRepository(session)

    async def get_by_id(self, advert_id: int):
        return await self.repo.get_by_id(advert_id)

    async def create(self, data: dict):
        advert = await self.repo.create(data)
        await self.session.commit()
        return advert

    async def update(self, advert_id: int, data: dict):
        advert = await self.repo.get_by_id(advert_id)
        if not advert:
            raise ValueError("Advert not found")

        advert = await self.repo.update(advert, data)
        await self.session.commit()
        return advert

    async def get_all(self):
        return await self.repo.get_all()

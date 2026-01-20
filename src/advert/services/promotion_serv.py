from ..repositories.promotion_repo import PromotionRepository
from sqlalchemy.ext.asyncio import AsyncSession

class PromotionService:

    def __init__(self, session: AsyncSession):

        self.session = session
        self.repo = PromotionRepository()
    async def create (self, data: dict):

        promotion = await self.repo.create(self.session,data)
        await self.session.commit()

        promotion = await  self.repo.get_by_advert_id(self.session, promotion.id)

        return promotion

    async def update_by_advert_id(self, advert_id: int, data: dict):
        """Обновление промоушена, привязанного к объявлению"""

        promotion = await self.repo.get_by_advert_id(self.session, advert_id)

        if not promotion:
            return None
 
        updated_promotion = await self.repo.update(self.session, promotion, data)


        await self.session.commit()
        await self.session.refresh(updated_promotion)

        return updated_promotion

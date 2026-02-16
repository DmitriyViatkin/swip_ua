from src.building.services.base import BaseService
from src.building.repositories.news import NewsRepository
from src.building.models.news import News
from sqlalchemy.ext.asyncio import AsyncSession


class NewsService(BaseService[News]):
    def __init__(self, repository: NewsRepository):
        super().__init__(repository)
    async def get_all_by_house(
            self,
            session: AsyncSession,
            house_id: int,
        ) -> list[News]:
            return await self.repository.get_all_by_house(session, house_id)
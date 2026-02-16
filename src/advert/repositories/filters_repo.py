from .advert_base_repo import  BaseRepository
from src.advert.models import Filter
from sqlalchemy import select


class FilterRepository(BaseRepository[Filter]):
    model = Filter

     
    async def get_active_filters_by_user(self, user_id: int):
        result = await self.session.execute(
            select(self.model).where(
                self.model.user_id == user_id,
                self.model.is_active == True
            )
        )
        return result.scalars().all()
from sqlalchemy.ext.asyncio import AsyncSession
from src.advert.repositories.filters_repo import FilterRepository
from src.advert.repositories.advert_repo import AdvertRepository
from src.advert.schemas.filters.filters_create_sch import FilterCreate
from src.advert.schemas.filters.filters_update_sch import FilterUpdate
from fastapi import HTTPException
from sqlalchemy import select, and_
from ..models.advert import Advert
from src.building.models.advantage_of_home import Advantages_of_Home
from src.building.models.house import House
from src.building.models.infrastructure import Infrastructure
from sqlalchemy.orm import selectinload

class FilterService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.filter_repo = FilterRepository(session)
        self.ad_repo = AdvertRepository(session)

    async def get_results_by_existing_filter(self, filter_id: int, user_id: int):
        db_filter = await self.filter_repo.get_by_id(filter_id)

        if not db_filter or db_filter.user_id != user_id:
            return None

        return await self.ad_repo.get_by_filter_params(db_filter)

    async def create_user_filter(self, user_id: int, filter_data: FilterCreate):
        data = filter_data.model_dump()
        data["user_id"] = user_id
        new_filter = await self.filter_repo.create(data)
        await self.session.commit()
        await self.session.refresh(new_filter)
        return new_filter

    async def create_filter_and_get_results(self, user_id: int, filter_dto: FilterCreate):
        """Зберігає фільтр та одразу повертає знайдені оголошення."""
        new_filter = await self.create_user_filter(user_id, filter_dto)
        # Використовуємо твій метод з AdvertRepository
        ads = await self.ad_repo.get_by_filter_params(new_filter)
        return {
            "filter": new_filter,
            "results": ads
        }

    async def update_filter(self, filter_id: int, user_id: int, update_data: FilterUpdate):
        db_filter = await self.filter_repo.get_by_id(filter_id)
        if not db_filter or db_filter.user_id != user_id:
            return None

        data = update_data.model_dump(exclude_unset=True)
        # ВИПРАВЛЕНО: прибираємо зайві дужки, передаємо об'єкт і словник
        update_obj = await self.filter_repo.update(db_filter, data)

        await self.session.commit()
        await self.session.refresh(update_obj)
        return update_obj

    async def delete_filter(self, filter_id: int, user_id: int):
        # 1. Отримуємо фільтр за ID
        db_filter = await self.filter_repo.get_by_id(filter_id)

        # ДІАГНОСТИКА (виведеться в консоль серверу)

        if not db_filter:

            raise HTTPException(status_code=404, detail="Фільтр не знайдено")



        # 2. Перевірка власності (приводимо до int про всяк випадок)
        if int(db_filter.user_id) != int(user_id):

            raise HTTPException(status_code=403, detail="Доступ заборонено: ви не є власником")



        # 3. Видалення та комміт
        await self.filter_repo.delete(db_filter)
        await self.session.commit()
        return True

    async def search(self, filter_data: FilterCreate):
        return await self.ad_repo.get_by_filter_params(filter_data)

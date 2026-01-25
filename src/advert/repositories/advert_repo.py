# src/advert/repositories/advert_repo.py




from .advert_base_repo import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, and_
from ..models.advert import Advert
from ..models.filters import Filter
from ..models.gallery import Gallery
from typing import Type
from sqlalchemy.orm import selectinload
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload

# Імпортуємо необхідні моделі
from src.advert.models.advert import Advert
from src.building.models.house import House
from src.building.models.infrastructure import Infrastructure
from src.building.models.advantage_of_home import Advantages_of_Home

FILTER_TO_ADVERT_MAP = {
    "housing_market": "housing_market", # Було "market_type", що викликало помилку
    "build_status": "build_status",
    "district": "district",
    "microdistrict": "microdistrict",
    "type_build": "type_build",
    "payment": "payment",
    "finishing": "finishing",
    "utility_bills": "utility_bills",
    "rooms": "rooms",
    "distance_to_the_sea": "distance_to_the_sea",
    "ceiling_height": "ceiling_height",
}
class AdvertRepository(BaseRepository[Advert]):
    model = Advert

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_by_build(self, build_id: int) -> list[Advert]:
        stmt = select(Advert).where(Advert.build_id == build_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, advert_id: int) -> Advert | None:
        stmt = (
            select(Advert)
            .where(Advert.id == advert_id)
            .options(
                selectinload(Advert.gallery)
                .selectinload(Gallery.images),
                selectinload(Advert.promotion),
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def exists(self, advert_id: int) -> bool:
        stmt = select(Advert.id).where(Advert.id == advert_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def set_gallery(self, advert_id: int, gallery_id: int):
        stmt = (
            update(Advert)
            .where(Advert.id == advert_id)
            .values(gallery_id=gallery_id)
        )
        await self.session.execute(stmt)
        await self.session.flush()

    async def get_by_id_with_gallery(self, advert_id: int):
        stmt = (
            select(Advert)
            .options(
                selectinload(Advert.gallery),
                selectinload(Advert.promotion),
            )
            .where(Advert.id == advert_id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_all(self):
        stmt = (
            select(Advert)
            .where((Advert.is_approved == True) & (Advert.is_active == True))
            .options(
                selectinload(Advert.promotion),  # загружаем промо заранее
                selectinload(Advert.gallery).selectinload(Gallery.images)  # галерея + картинки
            )
        )

        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, advert_id: int) -> Advert | None:
        stmt = (
            select(Advert)
            .where(Advert.id == advert_id)
            .options(
                selectinload(Advert.promotion),
                selectinload(Advert.gallery)
                .selectinload(Gallery.images)
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


    async def moderation(self, advert_id: int, status: bool):

        stmt = (update(Advert).where(Advert.id == advert_id).
                values(is_active=status, is_approved=status))
        await self.session.execute(stmt)
        await self.session.flush()
        return await self.get_by_id(advert_id)
    async def activation(self, advert_id: int, status: bool):

        stmt = (update(Advert).where(Advert.id == advert_id).
                values(is_active=status))
        await self.session.execute(stmt)
        await self.session.flush()
        return await self.get_by_id(advert_id)

    async def get_by_moderation (self):
        stmt = (
            select(Advert)
            .options(
                selectinload(Advert.gallery).selectinload(Gallery.images),
                selectinload(Advert.promotion),
            )
            .where(Advert.is_approved == False)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_filter_params(self, filter_obj):
        # 1. Створюємо базовий запит з усіма JOIN
        stmt = (
            select(self.model)
            .join(House, self.model.build_id == House.id)
            .join(Infrastructure, House.id == Infrastructure.house_id, isouter=True)
            .join(Advantages_of_Home, House.id == Advantages_of_Home.house_id, isouter=True)
        )

        # 2. Список базових умов
        conditions = [
            self.model.is_active == True,
            self.model.is_approved == True
        ]

        # --- Функція-помічник для безпечного отримання значень ---
        def get_val(name):
            return getattr(filter_obj, name, None)

        # --- Фільтрація по ADVERT (Прямі поля) ---
        if get_val("rooms") is not None:
            conditions.append(self.model.rooms == get_val("rooms"))

        if get_val("price_from"):
            conditions.append(self.model.price >= get_val("price_from"))
        if get_val("price_to"):
            conditions.append(self.model.price <= get_val("price_to"))

        if get_val("area_from"):
            conditions.append(self.model.area >= get_val("area_from"))
        if get_val("area_to"):
            conditions.append(self.model.area <= get_val("area_to"))

        # --- Фільтрація по INFRASTRUCTURE (Через House) ---
        if get_val("type_build"):
            conditions.append(Infrastructure.type_build == get_val("type_build"))

        if get_val("utility_bills"):
            conditions.append(Infrastructure.utility_bills == get_val("utility_bills"))

        if get_val("distance_to_the_sea"):
            conditions.append(Infrastructure.distance_to_sea <= get_val("distance_to_the_sea"))

        if get_val("ceiling_height"):
            conditions.append(Infrastructure.ceiling_height >= get_val("ceiling_height"))

        # --- Фільтрація по ADVANTAGES (Через House) ---
        # Навіть якщо цих полів немає в моделі Filter, код не впаде
        if get_val("is_parking") is not None:
            conditions.append(Advantages_of_Home.is_parking == get_val("is_parking"))

        # 3. Виконання запиту
        stmt = stmt.where(and_(*conditions)).distinct()
        stmt = stmt.options(
            selectinload(self.model.gallery),
            selectinload(self.model.promotion)
        )

        result = await self.session.execute(stmt)
        return result.scalars().all()



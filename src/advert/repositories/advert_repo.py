# src/advert/repositories/advert_repo.py




from .advert_base_repo import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, and_
from src.enums import TypeEnum
from ..models.gallery import Gallery

from sqlalchemy import select, and_, or_, desc,asc,nulls_last, case
from sqlalchemy.orm import selectinload

# Імпортуємо необхідні моделі
from src.advert.models.advert import Advert
from src.advert.models.promotion import Promotion
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
            select(Advert).outerjoin(Promotion)
            .where((Advert.is_approved == True) & (Advert.is_active == True))
            .options(
                selectinload(Advert.promotion),
                selectinload(Advert.gallery).selectinload(Gallery.images)
            ).order_by(
    case(
        (Promotion.type_promotion == TypeEnum.TURBO, 1),
        (Promotion.type_promotion == TypeEnum.UP, 2),
        else_=3
    ),
    desc(Advert.id)
            )
        )

        result = await self.session.execute(stmt)
        return result.scalars().unique().all()

    """async def get_by_id(self, advert_id: int) -> Advert | None:
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
        return result.scalar_one_or_none()"""


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

    async def get_by_filter_params(self, f):
        stmt = (
            select(Advert).outerjoin(Promotion)
            .outerjoin(House, Advert.build_id == House.id)
            .outerjoin(Infrastructure, House.id == Infrastructure.house_id)
            .outerjoin(Advantages_of_Home, House.id == Advantages_of_Home.house_id)
        )

        conditions = [
            Advert.is_active.is_(True),
            Advert.is_approved.is_(True),
        ]


        def val(name):
            return getattr(f, name, None)

        # ---- ADVERT ----
        if val("rooms") is not None:
            conditions.append(Advert.rooms == val("rooms"))

        if val("price_from") is not None:
            conditions.append(Advert.price >= val("price_from"))

        if val("price_to") is not None:
            conditions.append(Advert.price <= val("price_to"))

        if val("area_from") is not None:
            conditions.append(Advert.area >= val("area_from"))

        if val("area_to") is not None:
            conditions.append(Advert.area <= val("area_to"))

        # ---- INFRASTRUCTURE ----
        if val("type_build"):
            conditions.append(
                or_( Infrastructure.type_build == val("type_build"),
                    Infrastructure.id.is_(None)
                )
            )

        if val("utility_bills"):
            conditions.append(
                or_(
                    Infrastructure.utility_bills == val("utility_bills"),
                    Infrastructure.id.is_(None)
                )
            )

        if val("distance_to_the_sea"):
            conditions.append(
                or_(
                    Infrastructure.distance_to_sea <= val("distance_to_the_sea"),
                    Infrastructure.id.is_(None)
                )
            )

        if val("ceiling_height"):
            conditions.append(
                or_(
                    Infrastructure.ceiling_height >= val("ceiling_height"),
                    Infrastructure.id.is_(None)
                )
            )

        # ---- ADVANTAGES ----
        if val("is_parking") is not None:
            conditions.append(
                or_(
                    Advantages_of_Home.is_parking == val("is_parking"),
                    Advantages_of_Home.id.is_(None)
                )
            )

        stmt = (
            stmt
            .where(and_(*conditions))
            .options(
                selectinload(Advert.gallery),
                selectinload(Advert.promotion),
            ).order_by(
                        case(
                            (Promotion.type_promotion == TypeEnum.TURBO, 1),
                            (Promotion.type_promotion == TypeEnum.UP, 2),
                            else_=3
                        ),
                        desc(Advert.id)
                            ))



        result = await self.session.execute(stmt)
        return result.scalars().unique().all()



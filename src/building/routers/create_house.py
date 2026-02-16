from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from dishka.integrations.fastapi import FromDishka, inject
from src.auth.role_dependencies import require_roles
from src.auth.dependencies import get_current_user
from  src.enums import UserRole
from src.users.models.users import User
from src.building.schemas.house import HouseCreate, HouseRead
from src.building.services.house import HouseService
from src.advert.services.gallery_serv import GalleryService
from src.advert.services.gallery_image_service import GalleryImageService
from src.advert.repositories.gallery_image_repo import save_gallery_with_images

router = APIRouter()

@router.post(
    "/houses",
    response_model=HouseRead,
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_house(
    data: HouseCreate,
    session: FromDishka[AsyncSession],
    house_service: FromDishka[HouseService],
    gallery_service: FromDishka[GalleryService],
    gallery_image_service: FromDishka[GalleryImageService],
    current_user: User = Depends(require_roles(UserRole.DEV)),
):
    # 1️⃣ создаём дом без картинок
    house_data = data.dict(exclude={"images"})
    house_data["user_id"] = current_user.id
    house = await house_service.create(session, house_data)

    # 2️⃣ если есть картинки — создаём галерею
    if getattr(data, "images", None):
        try:
            # Если дома ещё нет gallery_id, передаем None
            gallery = await save_gallery_with_images(
                session=session,
                owner_id=house.id,
                owner_type="house",
                images=data.images,
                gallery_service=gallery_service,
                gallery_image_service=gallery_image_service,
                gallery_id=getattr(house, "gallery_id", None)
            )
            if gallery:
                house.gallery_id = gallery.id
                session.add(house)
                # 🔄 обновляем объект в сессии
                await session.flush()
        except Exception as e:
            print("Ошибка при сохранении картинок:", e)

    # 3️⃣ коммитим
    await session.commit()

    # 4️⃣ перечитываем дом с галереей и связями
    house = await house_service.get_by_id(session=session, pk=house.id)

    return house
